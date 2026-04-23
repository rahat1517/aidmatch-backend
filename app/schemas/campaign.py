from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CampaignCreate(BaseModel):
    title: str
    description: str | None = None
    location: str | None = None
    is_active: bool = True


class CampaignUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    is_active: bool | None = None


class CampaignResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    public_code: str
    title: str
    description: str | None = None
    location: str | None = None
    is_active: bool
    created_by: int
    created_at: datetime