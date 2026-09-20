from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.surplus import SurplusEventResponse
from app.models.surplus import SurplusEvent
from app.models.kitchen import Kitchen
from app.models.food_category import FoodCategory
from app.services.shelf_life_context import calculate_urgency
import datetime

router = APIRouter(prefix="/surplus", tags=["Surplus"])

@router.get("", response_model=list[SurplusEventResponse])
def get_surplus(kitchen_id: int = None, status: str = "", db: Session = Depends(get_db)):
    query = db.query(SurplusEvent, Kitchen, FoodCategory).join(
        Kitchen, SurplusEvent.kitchen_id == Kitchen.id
    ).join(
        FoodCategory, SurplusEvent.category_id == FoodCategory.id
    )
    
    if kitchen_id:
        query = query.filter(SurplusEvent.kitchen_id == kitchen_id)
        
    events = query.all()
    
    responses = []
    for se, kit, cat in events:
        if status and se.status.lower() != status.lower():
            continue
            
        remaining_hours, urgency = calculate_urgency(cat.name, se.batch_created_at)
        
        responses.append({
            "id": se.id,
            "kitchen_id": se.kitchen_id,
            "kitchen_name": kit.name,
            "category": cat.name,
            "is_vegetarian": cat.is_vegetarian,
            "quantity_kg": se.quantity_kg,
            "detected_at": se.detected_at.isoformat() if se.detected_at else "",
            "expiry_at": se.expiry_at.isoformat() if se.expiry_at else "",
            "rescue_window_hours": remaining_hours,
            "urgency_level": urgency,
            "status": se.status
        })
        
    # Sort by remaining_window_hours ASC, pushing EXPIRED to the bottom
    def sort_key(item):
        if item["urgency_level"] == "EXPIRED":
            return (1, item["rescue_window_hours"])
        return (0, item["rescue_window_hours"])
        
    responses.sort(key=sort_key)
    
    return [SurplusEventResponse(**r) for r in responses]
