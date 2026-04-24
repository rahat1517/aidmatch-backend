from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_admin
from app.schemas.item import ItemCreate, ItemUpdate, ItemUseRequest, ItemResponse
from app.services.item_service import (
    create_item,
    list_items_by_campaign,
    update_item,
    use_item,
    get_item_summary,
)

router = APIRouter()


@router.post("/campaign/{campaign_id}", response_model=ItemResponse)
def create_campaign_item(
    campaign_id: int,
    payload: ItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    return create_item(db, campaign_id, payload)


@router.get("/campaign/{campaign_id}", response_model=list[ItemResponse])
def get_campaign_items(
    campaign_id: int,
    db: Session = Depends(get_db),
):
    return list_items_by_campaign(db, campaign_id)


@router.put("/{item_id}", response_model=ItemResponse)
def update_campaign_item(
    item_id: int,
    payload: ItemUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    return update_item(db, item_id, payload)


@router.post("/{item_id}/use", response_model=ItemResponse)
def use_campaign_item(
    item_id: int,
    payload: ItemUseRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    return use_item(db, item_id, payload)


@router.get("/{item_id}/summary")
def get_campaign_item_summary(
    item_id: int,
    db: Session = Depends(get_db),
):
    return get_item_summary(db, item_id)