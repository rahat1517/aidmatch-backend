from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.core.security import decode_token
from app.core.firebase import verify_firebase_token

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:

    token = credentials.credentials

    # 1️⃣ try backend JWT
    payload = decode_token(token)
    if payload and "sub" in payload:
        try:
            user = db.query(User).filter(User.id == int(payload["sub"])).first()
            if user:
                return user
        except:
            pass

    # 2️⃣ try Firebase token
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