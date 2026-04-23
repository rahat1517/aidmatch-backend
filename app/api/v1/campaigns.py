from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_admin
from app.models.campaign import Campaign
from app.schemas.campaign import CampaignCreate, CampaignUpdate, CampaignResponse
from app.services.campaign_service import create_campaign, update_campaign, get_campaign_by_code

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


@router.post("/", response_model=CampaignResponse)
def create_campaign_route(
    payload: CampaignCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return create_campaign(db, payload, admin.id)


@router.get("/", response_model=list[CampaignResponse])
def list_campaigns(db: Session = Depends(get_db)):
    return db.query(Campaign).order_by(Campaign.id.desc()).all()


@router.get("/code/{public_code}", response_model=CampaignResponse)
def get_campaign_by_public_code(public_code: str, db: Session = Depends(get_db)):
    return get_campaign_by_code(db, public_code)


@router.put("/{campaign_id}", response_model=CampaignResponse)
def update_campaign_route(
    campaign_id: int,
    payload: CampaignUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return update_campaign(db, campaign_id, payload)