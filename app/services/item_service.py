from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.item import Item
from app.models.campaign import Campaign
from app.schemas.item import ItemCreate, ItemUpdate


def create_item(db: Session, campaign_id: int, payload: ItemCreate):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    item = Item(
        campaign_id=campaign_id,
        name=payload.name,
        unit=payload.unit,
        required_quantity=payload.required_quantity
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_item(db: Session, item_id: int, payload: ItemUpdate):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if payload.name is not None:
        item.name = payload.name
    if payload.unit is not None:
        item.unit = payload.unit
    if payload.required_quantity is not None:
        item.required_quantity = payload.required_quantity

    db.commit()
    db.refresh(item)
    return item


def get_item_summary(item: Item):
    available_stock = item.received_quantity - item.used_quantity
    remaining_need = item.required_quantity - item.used_quantity

    return {
        "item_id": item.id,
        "item_name": item.name,
        "unit": item.unit,
        "required_quantity": item.required_quantity,
        "received_quantity": item.received_quantity,
        "used_quantity": item.used_quantity,
        "available_stock": max(available_stock, 0),
        "remaining_need": max(remaining_need, 0)
    }


def use_item_quantity(db: Session, item_id: int, used_quantity: int):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    available_stock = item.received_quantity - item.used_quantity
    if used_quantity > available_stock:
        raise HTTPException(
            status_code=400,
            detail="Used quantity cannot exceed available stock"
        )

    item.used_quantity += used_quantity
    db.commit()
    db.refresh(item)
    return item