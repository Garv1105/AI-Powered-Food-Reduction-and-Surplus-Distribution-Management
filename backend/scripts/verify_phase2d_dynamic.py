import requests
import sys
import math
from datetime import datetime, timezone, timedelta
from sqlalchemy import create_engine, text

API_URL = "http://localhost:8002"
DB_URL = "sqlite:///test.db"

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def run_verification():
    print("==================================================")
    print(" PHASE 2D NGO MATCHING VERIFICATION SCRIPT")
    print("==================================================\n")
    
    engine = create_engine(DB_URL)

    with engine.connect() as conn:
        # Clear existing
        conn.execute(text("DELETE FROM surplus_events"))
        conn.execute(text("DELETE FROM ngos WHERE name='Test_NGO'"))
        conn.execute(text("DELETE FROM deliveries"))
        conn.commit()

        # Get Rice ID and K1 ID
        cat_id_rice = conn.execute(text("SELECT id FROM food_categories WHERE name='Rice'")).fetchone()[0]
        kit = conn.execute(text("SELECT id, lat, lng FROM kitchens WHERE name='K1_MainCampus'")).fetchone()
        kit_id, k_lat, k_lng = kit

        # Create Surplus Event for Rice (qty 50.0, fresh: 3.5h remaining)
        # Rice shelf life = 4.0. So 3.5h remaining = 0.5h ago
        now = datetime.now(timezone.utc)
        fresh_time = now - timedelta(hours=0.5)
        
        conn.execute(text(f"""
            INSERT INTO surplus_events (kitchen_id, category_id, quantity_kg, batch_created_at, urgency_level, status) 
            VALUES ({kit_id}, {cat_id_rice}, 50.0, '{fresh_time.isoformat()}', 'GREEN', 'ACTIVE')
        """))
        conn.commit()
        surplus_id = conn.execute(text("SELECT id FROM surplus_events ORDER BY id DESC LIMIT 1")).fetchone()[0]

        # Calculate exact coords for ~4km away
        # 1 deg lat ~ 111 km
        target_lat = k_lat + (4.0 / 111.0)
        
        # Insert Test NGO
        conn.execute(text(f"""
            INSERT INTO ngos (name, contact_name, contact_phone, lat, lng, capacity_kg, accepted_categories, operating_hours_start, operating_hours_end, is_active)
            VALUES ('Test_NGO', 'Tester', '0000', {target_lat}, {k_lng}, 100.0, 'Rice,Dal', '00:00', '23:59', 1)
        """))
        conn.commit()
        ngo_id = conn.execute(text("SELECT id FROM ngos WHERE name='Test_NGO'")).fetchone()[0]

        # Get exact straight-line distance
        straight_dist = haversine(k_lat, k_lng, target_lat, k_lng)

    print("Test 1: Base Scoring Math...")
    res = requests.get(f"{API_URL}/surplus/{surplus_id}/matches")
    assert res.status_code == 200, f"Failed API call: {res.text}"
    matches = res.json()
    
    test_match = next((m for m in matches if m["ngo_id"] == ngo_id), None)
    assert test_match, "Test NGO not found in matches!"
    
    # distance_km in API is the road distance (straight_dist * 1.5)
    api_road_dist = test_match["distance_km"]
    road_dist = straight_dist * 1.5
    
    dist_score = (1 - (road_dist / 15.0)) * 40
    cap_score = (50.0 / 100.0) * 25
    remaining_hours = 3.5
    time_margin = remaining_hours - ((road_dist / 20.0) + 0.5)
    time_score = (time_margin / remaining_hours) * 20
    expected_score = dist_score + cap_score + time_score + 15
    
    actual_score = test_match["match_score"]
    assert abs(actual_score - expected_score) < 0.2, f"FAILED: Expected {expected_score}, got {actual_score}"
    print(f"? SUCCESS: Base Scoring Math verified. Score = {actual_score}")

    print("\nTest 2: Capacity Hard Filter...")
    with engine.connect() as conn:
        conn.execute(text(f"UPDATE ngos SET capacity_kg = 40.0 WHERE id={ngo_id}"))
        conn.commit()
    
    res2 = requests.get(f"{API_URL}/surplus/{surplus_id}/matches")
    matches2 = res2.json()
    test_match2 = next((m for m in matches2 if m["ngo_id"] == ngo_id), None)
    assert test_match2 is None, "FAILED: NGO should be excluded due to low capacity."
    print("? SUCCESS: Capacity Hard Filter passed.")

    print("\nTest 3: Expiry/Travel Time Hard Filter...")
    with engine.connect() as conn:
        conn.execute(text(f"UPDATE ngos SET capacity_kg = 100.0 WHERE id={ngo_id}")) # Reset
        # Make remaining window = 0.6h. Shelf life = 4.0h. So batch created 3.4h ago.
        short_time = datetime.now(timezone.utc) - timedelta(hours=3.4)
        conn.execute(text(f"UPDATE surplus_events SET batch_created_at = '{short_time.isoformat()}' WHERE id={surplus_id}"))
        conn.commit()
        
    res3 = requests.get(f"{API_URL}/surplus/{surplus_id}/matches")
    matches3 = res3.json()
    test_match3 = next((m for m in matches3 if m["ngo_id"] == ngo_id), None)
    assert test_match3 is None, "FAILED: NGO should be excluded due to travel time > remaining window."
    print("? SUCCESS: Expiry/Travel Time Hard Filter passed.")

    print("\nTest 4: Load Balancing Penalty...")
    with engine.connect() as conn:
        conn.execute(text(f"UPDATE surplus_events SET batch_created_at = '{fresh_time.isoformat()}' WHERE id={surplus_id}"))
        conn.commit()
        
    # Baseline
    res4a = requests.get(f"{API_URL}/surplus/{surplus_id}/matches")
    baseline_score = next(m["match_score"] for m in res4a.json() if m["ngo_id"] == ngo_id)
    
    # Insert completed delivery today
    with engine.connect() as conn:
        now_ist_ish = datetime.now(timezone.utc)
        conn.execute(text(f"""
            INSERT INTO deliveries (surplus_event_id, ngo_id, status, delivered_at)
            VALUES ({surplus_id}, {ngo_id}, 'DELIVERED', '{now_ist_ish.isoformat()}')
        """))
        conn.commit()
        
    res4b = requests.get(f"{API_URL}/surplus/{surplus_id}/matches")
    new_score = next(m["match_score"] for m in res4b.json() if m["ngo_id"] == ngo_id)
    
    assert abs((baseline_score - 15.0) - new_score) < 0.2, f"FAILED: Expected penalty of 15. Baseline={baseline_score}, New={new_score}"
    print(f"? SUCCESS: Load Balancing Penalty passed. Score dropped from {baseline_score} to {new_score}.")

    print("\n==================================================")
    print(" ALL TESTS PASSED. PHASE 2D IS VERIFIED. ")
    print("==================================================")

if __name__ == "__main__":
    try:
        run_verification()
    except Exception as e:
        print(f"\n? VERIFICATION CRASHED: {e}")
        sys.exit(1)
