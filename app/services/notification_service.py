from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.models.user import User
from app.core.firebase import send_push_notification


def create_notification(db: Session, user_id: int, title: str, body: str):
    notification = Notification(
        user_id=user_id,
        title=title,
        body=body
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)

    user = db.query(User).filter(User.id == user_id).first()
    if user and user.fcm_token:
        send_push_notification(
            device_token=user.fcm_token,
            title=title,
            body=body,
            data={"user_id": user_id, "notification_id": notification.id}
        )

    return notification