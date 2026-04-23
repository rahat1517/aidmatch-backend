from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.campaign import Campaign
from app.schemas.campaign import CampaignCreate, CampaignUpdate
from app.utils.campaign_code import generate_campaign_code


def create_campaign(db: Session, payload: CampaignCreate, admin_id: int):
    campaign = Campaign(
        public_code=generate_campaign_code(db),
        title=payload.title,
        description=payload.description,
        location=payload.location,
        is_active=payload.is_active,
        created_by=admin_id
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


def update_campaign(db: Session, campaign_id: int, payload: CampaignUpdate):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    if payload.title is not None:
        campaign.title = payload.title
    if payload.description is not None:
        campaign.description = payload.description
    if payload.location is not None:
        campaign.location = payload.location
    if payload.is_active is not None:
        campaign.is_active = payload.is_active

    db.commit()
    db.refresh(campaign)
    return campaign


def get_campaign_by_code(db: Session, public_code: str):
    campaign = db.query(Campaign).filter(Campaign.public_code == public_code).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign