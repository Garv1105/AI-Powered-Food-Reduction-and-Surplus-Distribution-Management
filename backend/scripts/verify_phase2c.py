import requests
import sys
from datetime import datetime, timezone, timedelta
from sqlalchemy import create_engine, text

API_URL = "http://localhost:8002"
DB_URL = "sqlite:///test.db"

KITCHEN_ID_NAME = "K1_MainCampus"

def run_verification():
    print("==================================================")
    print(" PHASE 2C DYNAMIC VERIFICATION SCRIPT")
    print("==================================================\n")
    
    engine = create_engine(DB_URL)

    with engine.connect() as conn:
        # Clear existing surplus events to ensure a clean test
        conn.execute(text("DELETE FROM surplus_events"))
        conn.commit()
        
        # Get category_id for Rice and kitchen_id for K1_MainCampus
        cat_id_rice = conn.execute(text("SELECT id FROM food_categories WHERE name='Rice'")).fetchone()[0]
        kit_id = conn.execute(text(f"SELECT id FROM kitchens WHERE name='{KITCHEN_ID_NAME}'")).fetchone()[0]

        print("Test 1: Setup & DB Connection - OK")
        
        # Insert a single test SurplusEvent for Rice
        now = datetime.now(timezone.utc)
        conn.execute(text(f"""
            INSERT INTO surplus_events (kitchen_id, category_id, quantity_kg, batch_created_at, expiry_at, urgency_level, status) 
            VALUES ({kit_id}, {cat_id_rice}, 10.0, '{now.isoformat()}', '{now.isoformat()}', 'UNKNOWN', 'ACTIVE')
        """))
        conn.commit()
        
        event_id = conn.execute(text("SELECT id FROM surplus_events ORDER BY id DESC LIMIT 1")).fetchone()[0]

    # Helper function to update time and check api
    def test_tier(hours_ago, expected_urgency):
        with engine.connect() as conn:
            target_time = datetime.now(timezone.utc) - timedelta(hours=hours_ago)
            conn.execute(text(f"UPDATE surplus_events SET batch_created_at = '{target_time.isoformat()}' WHERE id = {event_id}"))
            conn.commit()
            
        res = requests.get(f"{API_URL}/surplus")
        assert res.status_code == 200, f"Failed GET /surplus: {res.text}"
        events = res.json()
        target_event = next(e for e in events if e["id"] == event_id)
        
        # Expected remaining window (Rice shelf life = 4 hours)
        expected_remaining = round(4.0 - hours_ago, 2)
        actual_remaining = target_event["rescue_window_hours"]
        
        # Tolerating small floating point differences due to script execution time
        assert abs(actual_remaining - expected_remaining) < 0.05, f"??? FAILED: Expected ~{expected_remaining}h, got {actual_remaining}h"
        assert target_event["urgency_level"] == expected_urgency, f"??? FAILED: Expected {expected_urgency}, got {target_event['urgency_level']}"
        print(f"? SUCCESS: Tested {expected_urgency} tier. Remaining hours = {actual_remaining}")

    # ---------------------------------------------------------
    # Test GREEN Tier
    # ---------------------------------------------------------
    print("\nTest 2: Test GREEN Tier (0.5h ago)...")
    test_tier(0.5, "GREEN")

    # ---------------------------------------------------------
    # Test AMBER Tier
    # ---------------------------------------------------------
    print("Test 3: Test AMBER Tier (2.0h ago)...")
    test_tier(2.0, "AMBER")

    # ---------------------------------------------------------
    # Test RED Tier
    # ---------------------------------------------------------
    print("Test 4: Test RED Tier (3.5h ago)...")
    test_tier(3.5, "RED")

    # ---------------------------------------------------------
    # Test EXPIRED Tier & Exclusion
    # ---------------------------------------------------------
    print("Test 5: Test EXPIRED Tier (5.0h ago) & Exclusion...")
    test_tier(5.0, "EXPIRED")
    
    # Assert dashboard summary does not include this EXPIRED event
    res_dash = requests.get(f"{API_URL}/dashboard/summary")
    assert res_dash.status_code == 200, f"Failed GET /dashboard/summary: {res_dash.text}"
    active_surplus_count = res_dash.json().get("active_surplus_count", -1)
    
    # We only have one event, and it is EXPIRED, so active count must be 0
    assert active_surplus_count == 0, f"??? FAILED: active_surplus_count should be 0 (excluding EXPIRED), got {active_surplus_count}"
    print("? SUCCESS: EXPIRED item is successfully excluded from Dashboard Active count.")

    # ---------------------------------------------------------
    # Test Complex Sorting
    # ---------------------------------------------------------
    print("\nTest 6: Test Complex Sorting (RED top, GREEN middle, EXPIRED bottom)...")
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM surplus_events"))
        conn.commit()
        
        # Insert 3 events
        now = datetime.now(timezone.utc)
        
        # GREEN (0.5 hours ago)
        time_green = now - timedelta(hours=0.5)
        # RED (3.5 hours ago)
        time_red = now - timedelta(hours=3.5)
        # EXPIRED (5.0 hours ago)
        time_expired = now - timedelta(hours=5.0)
        
        conn.execute(text(f"""
            INSERT INTO surplus_events (kitchen_id, category_id, quantity_kg, batch_created_at, urgency_level, status) 
            VALUES 
            ({kit_id}, {cat_id_rice}, 1.0, '{time_green.isoformat()}', 'UNKNOWN', 'ACTIVE'),
            ({kit_id}, {cat_id_rice}, 2.0, '{time_red.isoformat()}', 'UNKNOWN', 'ACTIVE'),
            ({kit_id}, {cat_id_rice}, 3.0, '{time_expired.isoformat()}', 'UNKNOWN', 'ACTIVE')
        """))
        conn.commit()
        
    res = requests.get(f"{API_URL}/surplus")
    events = res.json()
    
    # Assert there are 3 active events
    assert len(events) == 3, f"??? FAILED: Expected 3 events, got {len(events)}"
    
    # Assert order
    assert events[0]["urgency_level"] == "RED", f"??? FAILED: Expected RED at index 0, got {events[0]['urgency_level']}"
    assert events[1]["urgency_level"] == "GREEN", f"??? FAILED: Expected GREEN at index 1, got {events[1]['urgency_level']}"
    assert events[2]["urgency_level"] == "EXPIRED", f"??? FAILED: Expected EXPIRED at index 2, got {events[2]['urgency_level']}"
    print("? SUCCESS: Array correctly sorted: RED at top, GREEN middle, EXPIRED at bottom.")

    print("\n==================================================")
    print(" ALL TESTS PASSED. PHASE 2C IS VERIFIED. ")
    print("==================================================")

if __name__ == "__main__":
    try:
        run_verification()
    except Exception as e:
        print(f"\n? VERIFICATION CRASHED: {e}")
        sys.exit(1)
