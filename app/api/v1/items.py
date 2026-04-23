from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_admin
from app.models.item import Item
from app.schemas.item import (
    ItemCreate,
    ItemUpdate,
    ItemResponse,
    ItemUseRequest,
    ItemSummaryResponse
)
from app.services.item_service import create_item, update_item, use_item_quantity, get_item_summary

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/campaign/{campaign_id}", response_model=ItemResponse)
def create_item_route(
    campaign_id: int,
    payload: ItemCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return create_item(db, campaign_id, payload)


@router.get("/campaign/{campaign_id}", response_model=list[ItemResponse])
def list_items_by_campaign(campaign_id: int, db: Session = Depends(get_db)):
    return db.query(Item).filter(Item.campaign_id == campaign_id).order_by(Item.id.desc()).all()


@router.put("/{item_id}", response_model=ItemResponse)
def update_item_route(
    item_id: int,
    payload: ItemUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return update_item(db, item_id, payload)


@router.post("/{item_id}/use", response_model=ItemResponse)
def use_item_route(
    item_id: int,
    payload: ItemUseRequest,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return use_item_quantity(db, item_id, payload.used_quantity)


@router.get("/{item_id}/summary", response_model=ItemSummaryResponse)
def item_summary(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    return get_item_summary(item)