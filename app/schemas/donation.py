from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class DonationCreate(BaseModel):
    campaign_id: int
    item_id: int | None = None
    donation_type: str
    quantity: int | None = Field(default=None, ge=0)
    amount: float | None = Field(default=None, ge=0)
    donor_note: str | None = None


class DonationReceiveRequest(BaseModel):
    received_quantity: int | None = Field(default=None, ge=0)
    admin_note: str | None = None


class DonationRejectRequest(BaseModel):
    admin_note: str | None = None


class DonationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    donor_id: int
    campaign_id: int
    item_id: int | None = None
    donation_type: str
    status: str
    quantity: int | None = None
    amount: float | None = None
    donor_note: str | None = None
    admin_note: str | None = None
    recommendation_level: str | None = None
    recommendation_reason: str | None = None
    better_alternative: str | None = None
    suggested_quantity: int | None = None
    created_at: datetime
    received_at: datetime | None = None
    used_at: datetime | None = None