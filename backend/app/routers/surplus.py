from fastapi import APIRouter
from app.schemas.surplus import SurplusEventResponse
import datetime

router = APIRouter(prefix="/surplus", tags=["Surplus"])

@router.get("", response_model=list[SurplusEventResponse])
def get_surplus(kitchen_id: int = 1, status: str = ""):
    now = datetime.datetime.now(datetime.timezone.utc)
    
    stubs = [
        {
            "id": 1, "kitchen_id": 1, "kitchen_name": "BMTC Staff Canteen, Bengaluru",
            "category": "rice", "is_vegetarian": True, "quantity_kg": 12.5,
            "detected_at": (now - datetime.timedelta(minutes=30)).isoformat(),
            "expiry_at": (now + datetime.timedelta(hours=5.5)).isoformat(),
            "rescue_window_hours": 1.5, "urgency_level": "critical", "status": "pending"
        },
        {
            "id": 2, "kitchen_id": 1, "kitchen_name": "BMTC Staff Canteen, Bengaluru",
            "category": "vegetable_curry", "is_vegetarian": True, "quantity_kg": 8.0,
            "detected_at": (now - datetime.timedelta(minutes=45)).isoformat(),
            "expiry_at": (now + datetime.timedelta(hours=5.25)).isoformat(),
            "rescue_window_hours": 3.0, "urgency_level": "high", "status": "pending"
        },
        {
            "id": 3, "kitchen_id": 1, "kitchen_name": "BMTC Staff Canteen, Bengaluru",
            "category": "dal", "is_vegetarian": True, "quantity_kg": 5.5,
            "detected_at": (now - datetime.timedelta(minutes=60)).isoformat(),
            "expiry_at": (now + datetime.timedelta(hours=7)).isoformat(),
            "rescue_window_hours": 6.5, "urgency_level": "medium", "status": "matched"
        },
        {
            "id": 4, "kitchen_id": 1, "kitchen_name": "BMTC Staff Canteen, Bengaluru",
            "category": "dessert", "is_vegetarian": True, "quantity_kg": 3.0,
            "detected_at": (now - datetime.timedelta(minutes=15)).isoformat(),
            "expiry_at": (now + datetime.timedelta(hours=11.75)).isoformat(),
            "rescue_window_hours": 12.0, "urgency_level": "low", "status": "pending"
        }
    ]
    
    if status:
        stubs = [s for s in stubs if s["status"] == status]
        
    return [SurplusEventResponse(**s) for s in stubs]
