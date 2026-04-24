import os
from typing import Optional

import firebase_admin
from firebase_admin import credentials, messaging, auth

from app.core.config import settings


def init_firebase() -> None:
    if firebase_admin._apps:
        return

    credentials_path = settings.FIREBASE_CREDENTIALS_PATH

    if not credentials_path or not os.path.exists(credentials_path):
        print("Firebase credentials file not found. Firebase features disabled.")
        return

    try:
        cred = credentials.Certificate(credentials_path)
        firebase_admin.initialize_app(cred)
        print("Firebase initialized successfully.")
    except Exception as e:
        print(f"Firebase init error: {e}")


def verify_firebase_token(id_token: str) -> Optional[dict]:
    try:
        if not firebase_admin._apps:
            init_firebase()

        if not firebase_admin._apps:
            return None

        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(f"Firebase token verify error: {e}")
        return None


def send_push_notification(
    device_token: str,
    title: str,
    body: str,
    data: Optional[dict] = None
) -> Optional[str]:
    if not settings.FCM_ENABLED:
        print("FCM disabled. Notification skipped.")
        return None

    try:
        if not firebase_admin._apps:
            init_firebase()

        if not firebase_admin._apps:
            print("Firebase not initialized. Notification skipped.")
            return None

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            token=device_token,
            data={k: str(v) for k, v in (data or {}).items()}
        )

        response = messaging.send(message)
        return response

    except Exception as e:
        print(f"FCM send error: {e}")
        return None