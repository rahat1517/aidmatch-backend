import firebase_admin
from firebase_admin import credentials, auth
from app.core.config import settings


def init_firebase():
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
            print("Firebase initialized")
        except Exception as e:
            print(f"Firebase init error: {e}")


def verify_firebase_token(id_token: str):
    try:
        if not firebase_admin._apps:
            init_firebase()

        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(f"Firebase verify error: {e}")
        return None