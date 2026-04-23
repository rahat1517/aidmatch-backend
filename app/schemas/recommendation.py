from pydantic import BaseModel


class RecommendationRequest(BaseModel):
    campaign_id: int
    item_id: int | None = None
    donation_type: str
    quantity: int | None = None
    amount: float | None = None


class RecommendationResponse(BaseModel):
    recommendation_level: str
    reason: str
    better_alternative: str | None = None
    suggested_quantity: int | None = None