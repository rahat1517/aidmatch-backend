from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DonationCreate(BaseModel):
    campaign_id: int
    item_id: int
    donation_type: str = "item"
    quantity: int
    amount: float = 0
    donor_note: Optional[str] = None


class DonationReceiveRequest(BaseModel):
    received_quantity: int
    admin_note: Optional[str] = None


class DonationRejectRequest(BaseModel):
    admin_note: Optional[str] = None


class DonationUsedRequest(BaseModel):
    used_quantity: int


class DonationResponse(BaseModel):
    id: int
    donor_id: int
    campaign_id: int
    item_id: int
    donation_type: str
    status: str
    quantity: int
    amount: float
    donor_note: Optional[str] = None
    admin_note: Optional[str] = None
    recommendation_level: Optional[str] = None
    recommendation_reason: Optional[str] = None
    better_alternative: Optional[str] = None
    suggested_quantity: Optional[int] = None
    created_at: datetime
    received_at: Optional[datetime] = None
    used_at: Optional[datetime] = None

    class Config:
        from_attributes = True