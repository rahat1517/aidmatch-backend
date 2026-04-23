from datetime import datetime
from pydantic import BaseModel, ConfigDict


class FCMTokenUpdateRequest(BaseModel):
    fcm_token: str


class NotificationCreate(BaseModel):
    user_id: int
    title: str
    body: str


class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    body: str
    is_read: bool
    created_at: datetime