from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.auth import FirebaseSyncRequest

from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.auth import RegisterRequest, LoginRequest

def firebase_sync_user(db: Session, firebase_uid: str, payload: FirebaseSyncRequest):
    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()

    if user:
        user.full_name = payload.full_name
        user.email = payload.email
        user.role = payload.role
        user.location = payload.location
        db.commit()
        db.refresh(user)
        return user
    

    existing_user = db.query(User).filter(User.email == payload.email).first()

    if existing_user:
        existing_user.firebase_uid = firebase_uid
        existing_user.full_name = payload.full_name
        existing_user.role = payload.role
        existing_user.location = payload.location
        db.commit()
        db.refresh(existing_user)
        return existing_user

    user = User(
        firebase_uid=firebase_uid,
        full_name=payload.full_name,
        email=payload.email,
        password_hash=None,
        role=payload.role,
        location=payload.location,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def register_user(db: Session, payload: RegisterRequest):
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
        role=payload.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, payload: LoginRequest):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token(str(user.id))
    return {
        "access_token": token,
        "token_type": "bearer"
    }