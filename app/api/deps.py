from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.core.firebase import verify_firebase_token
from app.models.user import User
from app.models.enums import UserRole


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials

    # 1. Try backend JWT token
    payload = decode_token(token)
    if payload and "sub" in payload:
        try:
            user_id = int(payload["sub"])
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                return user
        except Exception:
            pass

    # 2. Try Firebase ID token
    decoded = verify_firebase_token(token)
    if decoded:
        firebase_uid = decoded.get("uid")
        if firebase_uid:
            user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
            if user:
                return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token"
    )


def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user