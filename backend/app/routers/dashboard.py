from fastapi import APIRouter
from app.schemas.dashboard import DashboardSummaryResponse, DailyStat
import datetime
import random

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary():
    today = datetime.datetime.now()
    
    trend = []
    for i in range(6, -1, -1):
        d = today - datetime.timedelta(days=i)
        kg_rescued = random.uniform(40, 60)
        trend.append(DailyStat(
            date=d.date().isoformat(),
            kg_rescued=kg_rescued,
            kg_wasted=random.uniform(5, 12),
            meals_served=int(kg_rescued / 0.35),
            co2_saved_kg=kg_rescued * 2.5
        ))
        
    return DashboardSummaryResponse(
        kg_rescued_today=47.5,
        kg_wasted_today=8.2,
        active_surplus_count=4,
        ngos_served_this_month=12,
        forecast_accuracy_pct=87.4,
        co2_saved_today_kg=118.75,
        cost_saved_today_inr=2375.0,
        weekly_trend=trend
    )
