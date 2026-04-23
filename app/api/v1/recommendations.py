from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse
from app.services.recommendation_service import get_recommendation

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.post("/", response_model=RecommendationResponse)
def get_recommendation_route(payload: RecommendationRequest, db: Session = Depends(get_db)):
    result = get_recommendation(
        db=db,
        campaign_id=payload.campaign_id,
        item_id=payload.item_id,
        donation_type=payload.donation_type,
        quantity=payload.quantity,
        amount=payload.amount
    )
    return result