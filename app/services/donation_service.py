from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.donation import Donation
from app.models.item import Item
from app.services.recommendation_service import get_recommendation


def create_donation(db: Session, donor_id: int, payload):
    recommendation = get_recommendation(db, payload)

    donation = Donation(
        donor_id=donor_id,
        campaign_id=payload.campaign_id,
        item_id=payload.item_id,
        donation_type=payload.donation_type,
        status="pending",
        quantity=payload.quantity,
        amount=payload.amount,
        donor_note=payload.donor_note,
        recommendation_level=recommendation["recommendation_level"],
        recommendation_reason=recommendation["reason"],
        better_alternative=recommendation["better_alternative"],
        suggested_quantity=recommendation["suggested_quantity"],
    )

    db.add(donation)
    db.commit()
    db.refresh(donation)
    return donation


def list_my_donations(db: Session, donor_id: int):
    return db.query(Donation).filter(Donation.donor_id == donor_id).all()


def receive_donation(db: Session, donation_id: int, payload):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()

    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")

    if donation.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending donations can be received"
        )

    if payload.received_quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Received quantity must be greater than 0"
        )

    item = db.query(Item).filter(Item.id == donation.item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.received_quantity += payload.received_quantity

    donation.status = "received"
    donation.received_at = datetime.utcnow()
    donation.admin_note = payload.admin_note

    db.commit()
    db.refresh(item)
    db.refresh(donation)

    return donation


def mark_donation_used(db: Session, donation_id: int, payload):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()

    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")

    if donation.status != "received":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only received donations can be used"
        )

    item = db.query(Item).filter(Item.id == donation.item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    used_quantity = payload.used_quantity

    if used_quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Used quantity must be greater than 0"
        )

    available_stock = item.received_quantity - item.used_quantity

    if used_quantity > available_stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough available stock"
        )

    item.used_quantity += used_quantity
    donation.status = "used"
    donation.used_at = datetime.utcnow()

    db.commit()
    db.refresh(item)
    db.refresh(donation)

    return donation


def reject_donation(db: Session, donation_id: int, payload):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()

    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")

    if donation.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending donations can be rejected"
        )

    donation.status = "rejected"
    donation.admin_note = payload.admin_note

    db.commit()
    db.refresh(donation)
    return donation