import sys
from pathlib import Path
import datetime
import pandas as pd
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.main import app
from app.services.anumaan_context import KITCHEN_LOCATION_MAP

client = TestClient(app)

def verify_integration():
    print("Verifying Phase 2a Integration...")

    # 1. Assert GET /forecast returns 404 (old stub removed)
    response = client.get("/forecast")
    assert response.status_code == 404, "Old /forecast endpoint should return 404"
    print("Pass: /forecast returned 404")

    # 2. Check lag features directly from restaurant_demand_28k.csv vs endpoint
    csv_path = Path(__file__).resolve().parent.parent.parent / "restaurant_demand_28k.csv"
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])

    test_kitchen = "K1_MainCampus"
    test_loc = KITCHEN_LOCATION_MAP[test_kitchen]
    
    # Pick a date from the end of the historical dataset (e.g. 2025-12-25)
    test_date_str = "2025-12-25"
    test_date = pd.to_datetime(test_date_str)
    
    # Compute manual lag features from df
    df_loc = df[df['Location_ID'] == test_loc].sort_values('Date')
    
    yesterday = test_date - pd.Timedelta(days=1)
    days_7_ago = test_date - pd.Timedelta(days=7)
    
    row_yesterday = df_loc[df_loc['Date'] == yesterday]
    val_yesterday = row_yesterday['Customer_Count'].values[0] if not row_yesterday.empty else 300.0
    
    row_7_ago = df_loc[df_loc['Date'] == days_7_ago]
    val_7_ago = row_7_ago['Customer_Count'].values[0] if not row_7_ago.empty else 300.0
    
    start_date = test_date - pd.Timedelta(days=7)
    ma7_df = df_loc[(df_loc['Date'] >= start_date) & (df_loc['Date'] <= yesterday)]
    val_ma7 = ma7_df['Customer_Count'].mean() if not ma7_df.empty else 300.0

    # Call endpoint for 2025-12-25
    response = client.get(f"/anumaan/forecast?kitchen_id={test_kitchen}&date={test_date_str}")
    assert response.status_code == 200, f"Error calling endpoint: {response.text}"
    
    data = response.json()
    derived = data['derived_features']
    
    # Tolerances because of floating point
    assert abs(derived['Demand_Yesterday'] - val_yesterday) < 0.1, f"Yesterday mismatch: {derived['Demand_Yesterday']} vs {val_yesterday}"
    assert abs(derived['Demand_7_Days_Ago'] - val_7_ago) < 0.1, f"7_days mismatch: {derived['Demand_7_Days_Ago']} vs {val_7_ago}"
    assert abs(derived['Demand_MA7'] - val_ma7) < 0.1, f"MA7 mismatch: {derived['Demand_MA7']} vs {val_ma7}"
    print("Pass: Auto-assembled lag features perfectly match raw CSV computation.")
    
    # 3. Test variability across kitchens and dates
    # Test kitchen 1, date 1 (Weekday)
    resp1 = client.get(f"/anumaan/forecast?kitchen_id=K1_MainCampus&date=2026-09-22")
    assert resp1.status_code == 200
    pred1 = resp1.json()['predicted_customers']

    # Test kitchen 1, date 2 (Weekend)
    resp2 = client.get(f"/anumaan/forecast?kitchen_id=K1_MainCampus&date=2026-09-27")
    assert resp2.status_code == 200
    pred2 = resp2.json()['predicted_customers']

    # Test kitchen 2, date 1
    resp3 = client.get(f"/anumaan/forecast?kitchen_id=K2_HostelBlockA&date=2026-09-22")
    assert resp3.status_code == 200
    pred3 = resp3.json()['predicted_customers']
    
    assert pred1 != pred2, f"Predictions should vary across dates (Got {pred1} and {pred2})"
    assert pred1 != pred3, f"Predictions should vary across kitchens (Got {pred1} and {pred3})"
    
    print("Pass: Predictions vary accurately across kitchens and dates (weekend/weekday).")
    print("All Phase 2a verification checks PASSED.")

if __name__ == "__main__":
    verify_integration()
