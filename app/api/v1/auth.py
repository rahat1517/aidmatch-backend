from fastapi import APIRouter, Depends, Header
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
    authorization: str | None = Header(None)
):
    # Temporary fallback for hackathon:
    # If Firebase Admin credentials are missing, token verification may fail.
    # In that case, use email as temporary firebase_uid so frontend can continue.
    firebase_uid = payload.email

    if authorization and authorization.startswith("Bearer "):
        id_token = authorization.split(" ")[1]
        decoded = verify_firebase_token(id_token)

        if decoded and decoded.get("uid"):
            firebase_uid = decoded["uid"]

    return firebase_sync_user(db, firebase_uid, payload)