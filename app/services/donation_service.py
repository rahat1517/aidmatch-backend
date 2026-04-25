from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.donation import Donation
from app.models.item import Item
from app.services.recommendation_service import get_recommendation


def create_donation(db: Session, donor_id: int, payload):
    recommendation = {
        "level": None,
        "reason": None,
        "better_alternative": None,
        "suggested_quantity": None,
    }

    try:
        recommendation = get_recommendation(db, payload) or recommendation
    except Exception:
        pass

    donation = Donation(
        donor_id=donor_id,
        campaign_id=payload.campaign_id,
        item_id=payload.item_id,
        donation_type=payload.donation_type,
        quantity=payload.quantity or 0,
        amount=payload.amount or 0,
        donor_note=payload.donor_note,
        status="pending",
        recommendation_level=recommendation.get("level"),
        recommendation_reason=recommendation.get("reason"),
        better_alternative=recommendation.get("better_alternative"),
        suggested_quantity=recommendation.get("suggested_quantity"),
    )

    db.add(donation)
    db.commit()
    db.refresh(donation)
    return donation


def list_my_donations(db: Session, donor_id: int):
    return (
        db.query(Donation)
        .filter(Donation.donor_id == donor_id)
        .order_by(Donation.id.desc())
        .all()
    )


def receive_donation(
    db: Session,
    donation_id: int,
    received_quantity: int,
    admin_note: str | None = None,
):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()

    if not donation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found",
        )

    if donation.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Donation already processed",
        )

    if received_quantity < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Received quantity cannot be negative",
        )

    donation.status = "received"
    donation.received_at = datetime.utcnow()
    donation.admin_note = admin_note
    donation.quantity = received_quantity

    # ✅ MAIN FIX:
    # তোমার items table এ stock column নাই।
    # আছে: received_quantity
    if donation.item_id is not None:
        item = db.query(Item).filter(Item.id == donation.item_id).first()

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found for this donation",
            )

        item.received_quantity = (item.received_quantity or 0) + received_quantity

    db.commit()
    db.refresh(donation)
    return donation


def reject_donation(
    db: Session,
    donation_id: int,
    admin_note: str | None = None,
):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()

    if not donation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found",
        )

    if donation.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Donation already processed",
        )

    donation.status = "rejected"
    donation.admin_note = admin_note

    db.commit()
    db.refresh(donation)
    return donation


def mark_donation_used(db: Session, donation_id: int):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()

    if not donation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found",
        )

    if donation.status != "received":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only received donations can be marked as used",
        )

    donation.status = "used"
    donation.used_at = datetime.utcnow()

    # ✅ used quantity update
    if donation.item_id is not None:
        item = db.query(Item).filter(Item.id == donation.item_id).first()

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found for this donation",
            )

        item.used_quantity = (item.used_quantity or 0) + (donation.quantity or 0)

    db.commit()
    db.refresh(donation)
    return donation