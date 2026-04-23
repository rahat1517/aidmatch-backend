from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User
from app.models.campaign import Campaign
from app.models.item import Item
from app.models.enums import UserRole
from app.utils.campaign_code import generate_campaign_code
from app.core.config import settings


def seed():
    db: Session = SessionLocal()

    try:
        admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
        if not admin:
            admin = User(
                full_name="AidMatch Admin",
                email=settings.ADMIN_EMAIL,
                password_hash=hash_password(settings.ADMIN_PASSWORD),
                role=UserRole.ADMIN.value,
                is_active=True
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print("Admin created")
        else:
            print("Admin already exists")

        donor = db.query(User).filter(User.email == "donor@aidmatch.com").first()
        if not donor:
            donor = User(
                full_name="Demo Donor",
                email="donor@aidmatch.com",
                password_hash=hash_password("donor12345"),
                role=UserRole.DONOR.value,
                is_active=True
            )
            db.add(donor)
            db.commit()
            db.refresh(donor)
            print("Demo donor created")
        else:
            print("Demo donor already exists")

        campaign = db.query(Campaign).filter(Campaign.title == "Flood Relief Dhaka").first()
        if not campaign:
            campaign = Campaign(
                public_code=generate_campaign_code(db),
                title="Flood Relief Dhaka",
                description="Emergency support for flood-affected families",
                location="Dhaka",
                is_active=True,
                created_by=admin.id
            )
            db.add(campaign)
            db.commit()
            db.refresh(campaign)
            print("Demo campaign created")
        else:
            print("Demo campaign already exists")

        existing_items = db.query(Item).filter(Item.campaign_id == campaign.id).count()
        if existing_items == 0:
            items = [
                Item(
                    campaign_id=campaign.id,
                    name="Rice",
                    unit="kg",
                    required_quantity=500,
                    received_quantity=100,
                    used_quantity=30
                ),
                Item(
                    campaign_id=campaign.id,
                    name="Water",
                    unit="bottle",
                    required_quantity=1000,
                    received_quantity=200,
                    used_quantity=50
                ),
                Item(
                    campaign_id=campaign.id,
                    name="Medicine Kit",
                    unit="kit",
                    required_quantity=120,
                    received_quantity=20,
                    used_quantity=5
                ),
            ]
            db.add_all(items)
            db.commit()
            print("Demo items created")
        else:
            print("Demo items already exist")

        print("Seeding complete")

    finally:
        db.close()


if __name__ == "__main__":
    seed()