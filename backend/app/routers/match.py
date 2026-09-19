from fastapi import APIRouter
from app.schemas.match import NGOMatchResponse, MatchRequest

router = APIRouter(prefix="/match", tags=["Match"])

@router.post("", response_model=list[NGOMatchResponse])
def get_matches(request: MatchRequest):
    return [
        NGOMatchResponse(
            ngo_id=1, name="Akshaya Patra Foundation", address="Chord Road, Rajajinagar",
            contact_name="Contact 1", food_preference="veg", capacity_kg=50.0,
            distance_km=2.3, match_score=0.97, capacity_match=True, food_pref_match=True,
            lat=12.9716, lng=77.5946
        ),
        NGOMatchResponse(
            ngo_id=2, name="Seva Sangha Trust", address="Koramangala 4th Block",
            contact_name="Contact 2", food_preference="either", capacity_kg=30.0,
            distance_km=4.1, match_score=0.85, capacity_match=True, food_pref_match=True,
            lat=12.9352, lng=77.6245
        ),
        NGOMatchResponse(
            ngo_id=3, name="Robin Hood Army Bengaluru", address="Indiranagar 100 Feet Road",
            contact_name="Contact 3", food_preference="either", capacity_kg=25.0,
            distance_km=5.8, match_score=0.78, capacity_match=True, food_pref_match=True,
            lat=12.9539, lng=77.6101
        ),
        NGOMatchResponse(
            ngo_id=4, name="Annadana Foundation", address="Malleswaram 18th Cross",
            contact_name="Contact 4", food_preference="veg", capacity_kg=40.0,
            distance_km=7.2, match_score=0.71, capacity_match=True, food_pref_match=True,
            lat=12.9856, lng=77.5741
        ),
        NGOMatchResponse(
            ngo_id=5, name="Namma Bengaluru Foundation", address="JP Nagar 6th Phase",
            contact_name="Contact 5", food_preference="nonveg", capacity_kg=20.0,
            distance_km=9.4, match_score=0.62, capacity_match=True, food_pref_match=False,
            lat=12.9165, lng=77.5823
        )
    ]
