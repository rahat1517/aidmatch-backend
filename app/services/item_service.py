from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.item import Item


def create_item(db: Session, campaign_id: int, payload):
    item = Item(
        campaign_id=campaign_id,
        name=payload.name,
        unit=payload.unit,
        required_quantity=payload.required_quantity,
        received_quantity=0,
        used_quantity=0,
    )

    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_items_by_campaign(db: Session, campaign_id: int):
    return db.query(Item).filter(Item.campaign_id == campaign_id).all()


def update_item(db: Session, item_id: int, payload):
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if hasattr(payload, "name") and payload.name is not None:
        item.name = payload.name

    if hasattr(payload, "unit") and payload.unit is not None:
        item.unit = payload.unit

    if hasattr(payload, "required_quantity") and payload.required_quantity is not None:
        item.required_quantity = payload.required_quantity

    db.commit()
    db.refresh(item)
    return item


def use_item(db: Session, item_id: int, payload):
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    available_stock = item.received_quantity - item.used_quantity

    if payload.used_quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Used quantity must be greater than 0"
        )

    if payload.used_quantity > available_stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough available stock"
        )

    item.used_quantity += payload.used_quantity

    db.commit()
    db.refresh(item)
    return item


def get_item_summary(db: Session, item_id: int):
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

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
        "remaining_need": max(remaining_need, 0),
    }