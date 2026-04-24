from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import FirebaseSyncRequest
from app.core.firebase import verify_firebase_token
from app.services.auth_service import firebase_sync_user
from app.schemas.user import UserResponse

router = APIRouter()


@router.post("/firebase-sync", response_model=UserResponse)
def firebase_sync(
    payload: FirebaseSyncRequest,
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Firebase token"
        )

    id_token = authorization.split(" ")[1]

    decoded = verify_firebase_token(id_token)

    if not decoded:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Firebase token"
        )

    firebase_uid = decoded.get("uid")

    if not firebase_uid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Firebase token payload"
        )

    return firebase_sync_user(db, firebase_uid, payload)