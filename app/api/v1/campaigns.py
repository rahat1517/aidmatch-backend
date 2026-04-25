import random
import string

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_admin
from app.models.user import User
from app.models.campaign import Campaign
from app.schemas.campaign import CampaignCreate, CampaignResponse

router = APIRouter()


def generate_public_code(length: int = 4) -> str:
    return "AM-" + "".join(random.choices(string.digits, k=length))


@router.get("/", response_model=list[CampaignResponse])
def list_campaigns(db: Session = Depends(get_db)):
    return db.query(Campaign).filter(Campaign.is_active == True).all()


@router.post("/", response_model=CampaignResponse)
def create_campaign(
    payload: CampaignCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    public_code = generate_public_code()

    while db.query(Campaign).filter(Campaign.public_code == public_code).first():
        public_code = generate_public_code()

    campaign = Campaign(
        public_code=public_code,
        title=payload.title,
        description=payload.description,
        location=payload.location,
        is_active=True,
        created_by=current_admin.id,
    )

    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


@router.get("/code/{public_code}", response_model=CampaignResponse)
def get_campaign_by_code(
    public_code: str,
    db: Session = Depends(get_db),
):
    campaign = db.query(Campaign).filter(Campaign.public_code == public_code).first()

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    return campaign


@router.put("/{campaign_id}", response_model=CampaignResponse)
def update_campaign(
    campaign_id: int,
    payload: CampaignCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    campaign.title = payload.title
    campaign.description = payload.description
    campaign.location = payload.location
    campaign.is_active = payload.is_active

    db.commit()
    db.refresh(campaign)
    return campaign