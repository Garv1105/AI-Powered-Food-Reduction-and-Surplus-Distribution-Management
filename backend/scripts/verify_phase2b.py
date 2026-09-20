import requests
import sys
import os
from sqlalchemy import create_engine, text

# ==========================================
# CONFIGURATION
# ==========================================
API_URL = "http://localhost:8002"
DB_URL = "sqlite:///test.db" 

KITCHEN_ID = "K1_MainCampus"
DATE = "2026-09-25"

# The Stated Assumptions for Phase 2b
EXPECTED_RATES = {
    "Rice": 0.18, "Dal": 0.12, "Vegetable_Curry": 0.15, 
    "Roti_Bread": 2.0, "Salad": 0.06, "Dessert": 0.05, 
    "Beverages": 0.25, "Snacks": 0.08
}
SPOILAGE_RATE_RICE = 0.02 # Assuming 2% spoilage for Rice

def run_verification():
    print("==================================================")
    print(" PHASE 2B VERIFICATION SCRIPT")
    print("==================================================\n")
    
    engine = create_engine(DB_URL)

    # ---------------------------------------------------------
    # TEST 1: The "No Manual Surplus" Rule
    # ---------------------------------------------------------
    print("Test 1: Verifying absence of manual surplus calculation route...")
    res = requests.post(f"{API_URL}/calculate-surplus")
    assert res.status_code == 404, f"❌ FAILED: Found a route at /calculate-surplus. It must be deleted. (Got {res.status_code})"
    print("✅ SUCCESS: /calculate-surplus is correctly absent (404).\n")

    # ---------------------------------------------------------
    # TEST 2: Generation & Proportional Math
    # ---------------------------------------------------------
    print("Test 2: Verifying Production Plan math and proportionality...")
    res = requests.get(f"{API_URL}/production-plan/generate", params={"kitchen_id": KITCHEN_ID, "date": DATE})
    assert res.status_code == 200, f"❌ FAILED to generate plan: {res.text}"
    
    plan_data = res.json()
    categories = plan_data.get("categories", plan_data) 
    
    cat_dict = {item["category_name"]: item["predicted_qty"] for item in categories}
    
    for cat in EXPECTED_RATES.keys():
        assert cat in cat_dict, f"❌ FAILED: Missing category {cat} in production plan."
        
    expected_ratio = EXPECTED_RATES["Rice"] / EXPECTED_RATES["Dal"]
    actual_ratio = cat_dict["Rice"] / cat_dict["Dal"]
    
    assert abs(expected_ratio - actual_ratio) < 0.01, f"❌ FAILED: Proportionality mismatch. Expected Rice/Dal ratio {expected_ratio:.2f}, got {actual_ratio:.2f}"
    print(f"✅ SUCCESS: Math verified. Footfall correctly converted using standard rates (Rice/Dal ratio: {actual_ratio:.2f}).\n")

    # ---------------------------------------------------------
    # TEST 3: Save Plan (Freeze target for evening math)
    # ---------------------------------------------------------
    print("Test 3: Freezing the Production Plan...")
    save_payload = plan_data
    res = requests.post(f"{API_URL}/production-plan/save", json=save_payload)
    assert res.status_code in [200, 201], f"❌ FAILED to save plan: {res.text}"
    print("✅ SUCCESS: Plan saved successfully.\n")

    # ---------------------------------------------------------
    # TEST 4: Auto-Surplus Generation (No ghost production)
    # ---------------------------------------------------------
    print("Test 4: Logging initial consumption and verifying instant DB trigger...")
    log_payload_1 = {
        "kitchen_id": KITCHEN_ID,
        "date": DATE,
        "category_name": "Rice",
        "consumed_qty": 10.0
    }
    res = requests.post(f"{API_URL}/log-consumption", json=log_payload_1)
    assert res.status_code in [200, 201], f"❌ FAILED to log consumption: {res.text}"

    with engine.connect() as conn:
        # Get category_id for Rice and kitchen_id
        cat_id = conn.execute(text("SELECT id FROM food_categories WHERE name='Rice'")).fetchone()[0]
        kit_id = conn.execute(text(f"SELECT id FROM kitchens WHERE name='{KITCHEN_ID}'")).fetchone()[0]

        result = conn.execute(text(
            f"SELECT count(*), MAX(quantity_kg) FROM surplus_events WHERE category_id = {cat_id} AND date(batch_created_at) = '{DATE}' AND kitchen_id = {kit_id}"
        )).fetchone()
        
        count_1, surplus_1 = result[0], result[1]
        assert count_1 == 1, f"❌ FAILED: Expected 1 surplus event in DB, found {count_1}."
        print(f"✅ SUCCESS: Surplus auto-generated on first log. (Qty: {surplus_1})\n")

    # ---------------------------------------------------------
    # TEST 5: The "Double-Click" Idempotency Test
    # ---------------------------------------------------------
    print("Test 5: Logging corrected consumption to verify UPSERT idempotency...")
    log_payload_2 = {
        "kitchen_id": KITCHEN_ID,
        "date": DATE,
        "category_name": "Rice",
        "consumed_qty": 15.0
    }
    res = requests.post(f"{API_URL}/log-consumption", json=log_payload_2)
    assert res.status_code in [200, 201], f"❌ FAILED to log updated consumption: {res.text}"

    with engine.connect() as conn:
        result = conn.execute(text(
            f"SELECT count(*), MAX(quantity_kg) FROM surplus_events WHERE category_id = {cat_id} AND date(batch_created_at) = '{DATE}' AND kitchen_id = {kit_id}"
        )).fetchone()
        
        count_2, surplus_2 = result[0], result[1]
        assert count_2 == 1, f"❌ FAILED: Idempotency bug! Found {count_2} surplus events instead of 1. You used INSERT instead of UPSERT."
        assert surplus_2 < surplus_1, f"❌ FAILED: Surplus quantity did not update gracefully. (Old: {surplus_1}, New: {surplus_2})"
        print(f"✅ SUCCESS: Upsert worked! Row count is still {count_2}, Surplus correctly reduced from {surplus_1} to {surplus_2}.\n")

    print("==================================================")
    print(" ALL TESTS PASSED. PHASE 2B IS VERIFIED. ")
    print("==================================================")

if __name__ == "__main__":
    try:
        run_verification()
    except Exception as e:
        print(f"\n🚨 VERIFICATION CRASHED: {e}")
        sys.exit(1)
