import random
from sqlalchemy.orm import Session

from app.models.campaign import Campaign


def generate_campaign_code(db: Session) -> str:
    while True:
        code = f"AM-{random.randint(1000, 9999)}"
        exists = db.query(Campaign).filter(Campaign.public_code == code).first()
        if not exists:
            return code