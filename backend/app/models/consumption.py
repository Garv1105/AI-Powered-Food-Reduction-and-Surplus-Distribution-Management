from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class ConsumptionLog(Base):
    __tablename__ = "consumption_logs"

    id = Column(Integer, primary_key=True, index=True)
    kitchen_id = Column(Integer, ForeignKey("kitchens.id"))
    category_id = Column(Integer, ForeignKey("food_categories.id"))
    date = Column(Date, nullable=False)
    meal_type = Column(String(20))
    quantity_kg = Column(Float)
    headcount = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
