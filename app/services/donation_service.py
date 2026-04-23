from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.campaign import Campaign
from app.models.item import Item
from app.models.donation import Donation
from app.models.enums import DonationStatus
from app.schemas.donation import DonationCreate
from app.services.recommendation_service import get_recommendation
from app.services.notification_service import create_notification


def create_donation(db: Session, donor_id: int, payload: DonationCreate):
    campaign = db.query(Campaign).filter(Campaign.id == payload.campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    item = None
    if payload.item_id:
        item = db.query(Item).filter(
            Item.id == payload.item_id,
            Item.campaign_id == payload.campaign_id
        ).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found in campaign")

    recommendation = get_recommendation(
        db=db,
        campaign_id=payload.campaign_id,
        item_id=payload.item_id,
        donation_type=payload.donation_type,
        quantity=payload.quantity,
        amount=payload.amount
    )

    donation = Donation(
        donor_id=donor_id,
        campaign_id=payload.campaign_id,
        item_id=payload.item_id,
        donation_type=payload.donation_type,
        quantity=payload.quantity,
        amount=payload.amount,
        donor_note=payload.donor_note,
        recommendation_level=recommendation["recommendation_level"],
        recommendation_reason=recommendation["reason"],
        better_alternative=recommendation["better_alternative"],
        suggested_quantity=recommendation["suggested_quantity"],
        status=DonationStatus.PENDING.value
    )

    db.add(donation)
    db.commit()
    db.refresh(donation)

    create_notification(
        db,
        donor_id,
        "Donation submitted",
        f"Your donation for campaign {campaign.public_code} is now pending review."
    )

    return donation


def receive_donation(
    db: Session,
    donation_id: int,
    received_quantity: int | None = None,
    admin_note: str | None = None
):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")

    if donation.status != DonationStatus.PENDING.value:
        raise HTTPException(status_code=400, detail="Only pending donations can be received")

    if donation.donation_type in ["item", "kit"] and donation.item_id:
        item = db.query(Item).filter(Item.id == donation.item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        qty_to_receive = received_quantity if received_quantity is not None else (donation.quantity or 0)
        item.received_quantity += qty_to_receive

    donation.status = DonationStatus.RECEIVED.value
    donation.received_at = datetime.utcnow()
    donation.admin_note = admin_note

    db.commit()
    db.refresh(donation)

    create_notification(
        db,
        donation.donor_id,
        "Donation received",
        f"Your donation #{donation.id} has been marked as received."
    )

    return donation


def reject_donation(db: Session, donation_id: int, admin_note: str | None = None):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")

    if donation.status != DonationStatus.PENDING.value:
        raise HTTPException(status_code=400, detail="Only pending donations can be rejected")

    donation.status = DonationStatus.REJECTED.value
    donation.admin_note = admin_note
    db.commit()
    db.refresh(donation)

    create_notification(
        db,
        donation.donor_id,
        "Donation rejected",
        f"Your donation #{donation.id} was rejected."
    )

    return donation


def mark_donation_used(db: Session, donation_id: int):
    donation = db.query(Donation).filter(Donation.id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")

    if donation.status != DonationStatus.RECEIVED.value:
        raise HTTPException(status_code=400, detail="Only received donations can be marked as used")

    donation.status = DonationStatus.USED.value
    donation.used_at = datetime.utcnow()

    db.commit()
    db.refresh(donation)

    create_notification(
        db,
        donation.donor_id,
        "Donation used",
        f"Your donation #{donation.id} has been used for beneficiaries."
    )

    return donation