import os
from typing import Optional

import firebase_admin
from firebase_admin import credentials, messaging

from app.core.config import settings


def init_firebase() -> None:
    if not settings.FCM_ENABLED:
        return

    if firebase_admin._apps:
        return

    if not os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
        print("Firebase credentials file not found. Skipping Firebase init.")
        return

    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)
    print("Firebase initialized successfully.")


def send_push_notification(
    device_token: str,
    title: str,
    body: str,
    data: Optional[dict] = None
) -> Optional[str]:
    if not settings.FCM_ENABLED:
        print("FCM disabled. Notification skipped.")
        return None

    if not firebase_admin._apps:
        print("Firebase not initialized. Notification skipped.")
        return None

    try:
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