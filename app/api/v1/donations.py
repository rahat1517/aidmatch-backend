from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user, get_current_admin
from app.models.donation import Donation
from app.schemas.donation import (
    DonationCreate,
    DonationResponse,
    DonationReceiveRequest,
    DonationRejectRequest
)
from app.services.donation_service import (
    create_donation,
    receive_donation,
    reject_donation,
    mark_donation_used
)

router = APIRouter(prefix="/donations", tags=["Donations"])


@router.post("/", response_model=DonationResponse)
def create_donation_route(
    payload: DonationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_donation(db, current_user.id, payload)


@router.get("/my", response_model=list[DonationResponse])
def my_donations(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Donation).filter(Donation.donor_id == current_user.id).order_by(Donation.id.desc()).all()


@router.get("/", response_model=list[DonationResponse])
def all_donations(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return db.query(Donation).order_by(Donation.id.desc()).all()


@router.post("/{donation_id}/receive", response_model=DonationResponse)
def receive_donation_route(
    donation_id: int,
    payload: DonationReceiveRequest,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return receive_donation(db, donation_id, payload.received_quantity, payload.admin_note)


@router.post("/{donation_id}/reject", response_model=DonationResponse)
def reject_donation_route(
    donation_id: int,
    payload: DonationRejectRequest,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return reject_donation(db, donation_id, payload.admin_note)


@router.post("/{donation_id}/used", response_model=DonationResponse)
def mark_used_route(
    donation_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return mark_donation_used(db, donation_id)