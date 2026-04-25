from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest, FirebaseSyncRequest


ALLOWED_ROLES = {"admin", "donor"}


def register_user(db: Session, payload: RegisterRequest):
    role = payload.role or "donor"

    if role not in ALLOWED_ROLES:
        raise HTTPException(status_code=400, detail="Invalid role")

    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=role,
        location=getattr(payload, "location", None),
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, payload: LoginRequest):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not user.password_hash:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(str(user.id))

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
            "location": user.location,
        }
    }


def firebase_sync_user(db: Session, firebase_uid: str, payload: FirebaseSyncRequest):
    # Existing firebase user check
    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()

    if user:
        user.full_name = payload.full_name or user.full_name
        user.email = payload.email or user.email
        user.location = payload.location or user.location

        # Existing user role NEVER overwrite
        db.commit()
        db.refresh(user)
        return user

    # Existing email user check
    existing_user = db.query(User).filter(User.email == payload.email).first()

    if existing_user:
        existing_user.firebase_uid = firebase_uid
        existing_user.full_name = payload.full_name or existing_user.full_name
        existing_user.location = payload.location or existing_user.location

        # Existing email user role NEVER overwrite
        db.commit()
        db.refresh(existing_user)
        return existing_user

    # New Firebase user create
    # Role missing hole donor
    role = payload.role or "donor"

    if role not in ALLOWED_ROLES:
        raise HTTPException(status_code=400, detail="Invalid role")

    user = User(
        firebase_uid=firebase_uid,
        full_name=payload.full_name,
        email=payload.email,
        password_hash=None,
        role=role,
        location=payload.location,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user