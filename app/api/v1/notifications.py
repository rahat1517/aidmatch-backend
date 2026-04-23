from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.notification import Notification
from app.schemas.notification import FCMTokenUpdateRequest, NotificationResponse

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/my", response_model=list[NotificationResponse])
def get_my_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(Notification.id.desc()).all()


@router.post("/fcm-token")
def update_fcm_token(
    payload: FCMTokenUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    current_user.fcm_token = payload.fcm_token
    db.commit()
    db.refresh(current_user)
    return {"message": "FCM token updated successfully"}