from fastapi import APIRouter
from app.schemas.route import RouteResponse, Waypoint

router = APIRouter(prefix="/route", tags=["Route"])

@router.get("", response_model=RouteResponse)
def get_route(delivery_id: int = 1):
    k_lat, k_lng = 12.9600, 77.5800
    n_lat, n_lng = 12.9716, 77.5946
    
    waypoints = [
        Waypoint(lat=k_lat, lng=k_lng, label="BMTC Canteen", type="kitchen"),
        Waypoint(lat=12.9650, lng=77.5870, label="Checkpoint", type="waypoint"),
        Waypoint(lat=n_lat, lng=n_lng, label="Akshaya Patra", type="ngo")
    ]
    
    polyline = []
    steps = 8
    for i in range(steps):
        f = i / (steps - 1)
        lat = k_lat + (n_lat - k_lat) * f
        lng = k_lng + (n_lng - k_lng) * f
        polyline.append([lat, lng])
        
    return RouteResponse(
        delivery_id=delivery_id,
        waypoints=waypoints,
        total_distance_km=2.3,
        eta_minutes=18,
        route_polyline=polyline
    )
