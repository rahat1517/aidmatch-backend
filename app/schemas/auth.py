from pydantic import BaseModel, EmailStr


class FirebaseSyncRequest(BaseModel):
    full_name: str
    email: EmailStr
    role: str = "donor"
    location: str | None = None