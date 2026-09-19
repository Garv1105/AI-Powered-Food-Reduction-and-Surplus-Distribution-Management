from fastapi import APIRouter
from app.schemas.forecast import ForecastResponse, ForecastPoint
import datetime
import random

router = APIRouter(prefix="/forecast", tags=["Forecast"])

@router.get("", response_model=ForecastResponse)
def get_forecast(kitchen_id: int = 1, category: str = "rice", days_ahead: int = 7):
    base_values = {
        "rice": 45, "dal": 30, "vegetable_curry": 35, 
        "roti": 40, "salad": 15, "dessert": 20, 
        "sambar": 25, "milk": 20
    }
    
    base = base_values.get(category, 30)
    
    predictions = []
    today = datetime.datetime.now()
    
    random.seed(42 + kitchen_id + len(category))
    
    for i in range(days_ahead):
        pred_date = today + datetime.timedelta(days=i)
        variation = random.uniform(-0.05, 0.05)
        predicted_kg = base * (1 + variation)
        predictions.append(ForecastPoint(
            date=pred_date.date().isoformat(),
            predicted_kg=predicted_kg,
            confidence_lower=predicted_kg * 0.92,
            confidence_upper=predicted_kg * 1.08
        ))
        
    return ForecastResponse(
        kitchen_id=kitchen_id,
        category=category,
        unit="kg",
        generated_at=today.isoformat(),
        predictions=predictions
    )
