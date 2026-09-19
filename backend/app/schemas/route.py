from pydantic import BaseModel

class Waypoint(BaseModel):
    lat: float
    lng: float
    label: str
    type: str

class RouteResponse(BaseModel):
    delivery_id: int
    waypoints: list[Waypoint]
    total_distance_km: float
    eta_minutes: int
    route_polyline: list[list[float]]
