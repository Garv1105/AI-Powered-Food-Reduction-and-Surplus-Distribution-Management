"""
Anumaan router — POST /predict-demand
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas.anumaan import PredictDemandRequest, PredictDemandResponse
from app.services import anumaan as anumaan_service

router = APIRouter(prefix="/anumaan", tags=["Anumaan"])


@router.post(
    "/predict-demand",
    response_model=PredictDemandResponse,
    summary="Predict customer demand for a given date and location",
    description=(
        "Accepts kitchen manager inputs and returns Anumaan's predicted "
        "customer count for the specified date and location, plus derived "
        "diagnostic features. `recommended_production` and `expected_surplus` "
        "are stubs until the production planning module is built."
    ),
)
def predict_demand(request: PredictDemandRequest) -> PredictDemandResponse:
    """
    Run one Anumaan demand prediction.

    Raises
    ------
    HTTP 422  — automatic on Pydantic validation failure (invalid field values)
    HTTP 400  — if location_id is unknown (secondary guard; Pydantic catches first)
    HTTP 503  — if the model file is missing or xgboost is not installed
    """
    try:
        inputs = request.model_dump()
        predicted_customers, derived_features = anumaan_service.predict(inputs)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except (FileNotFoundError, RuntimeError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return PredictDemandResponse(
        predicted_customers=predicted_customers,
        recommended_production=None,  # stub
        expected_surplus=None,         # stub
        location_id=request.location_id,
        date=request.date,
        derived_features=derived_features,
    )
