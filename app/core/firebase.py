import json
import os
from typing import Optional

import firebase_admin
from firebase_admin import auth, credentials, messaging

from app.core.config import settings


def init_firebase() -> None:
    if firebase_admin._apps:
        return

    try:
        cred_json = os.getenv("FIREBASE_CREDENTIALS_JSON")

        if cred_json:
            cred_dict = json.loads(cred_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            print("Firebase initialized from env JSON.")
            return

        credentials_path = getattr(settings, "FIREBASE_CREDENTIALS_PATH", None)

        if credentials_path and os.path.exists(credentials_path):
            cred = credentials.Certificate(credentials_path)
            firebase_admin.initialize_app(cred)
            print("Firebase initialized from file.")
            return

        print("Firebase credentials not found. Firebase features disabled.")

    except Exception as e:
        print(f"Firebase init error: {e}")


def verify_firebase_token(id_token: str) -> Optional[dict]:
    try:
        if not firebase_admin._apps:
            init_firebase()

        if not firebase_admin._apps:
            return None

        return auth.verify_id_token(id_token)

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
            return None

        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            token=device_token,
            data={k: str(v) for k, v in (data or {}).items()}
        )

        return messaging.send(message)

    except Exception as e:
        print(f"FCM send error: {e}")
        return None