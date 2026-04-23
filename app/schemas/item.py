from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    unit: str = Field(default="pcs", min_length=1, max_length=50)
    required_quantity: int = Field(..., ge=0)


class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    unit: str | None = Field(default=None, min_length=1, max_length=50)
    required_quantity: int | None = Field(default=None, ge=0)


class ItemUseRequest(BaseModel):
    used_quantity: int = Field(..., gt=0)


class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    campaign_id: int
    name: str
    unit: str
    required_quantity: int
    received_quantity: int
    used_quantity: int
    created_at: datetime


class ItemSummaryResponse(BaseModel):
    item_id: int
    item_name: str
    unit: str
    required_quantity: int
    received_quantity: int
    used_quantity: int
    available_stock: int
    remaining_need: int