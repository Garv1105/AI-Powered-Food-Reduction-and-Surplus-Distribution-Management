from pydantic import BaseModel

class ForecastPoint(BaseModel):
    date: str
    predicted_kg: float
    confidence_lower: float
    confidence_upper: float

class ForecastResponse(BaseModel):
    kitchen_id: int
    category: str
    unit: str
    generated_at: str
    predictions: list[ForecastPoint]
