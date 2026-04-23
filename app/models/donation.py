from datetime import datetime

from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import DonationStatus, DonationType


class Donation(Base):
    __tablename__ = "donations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    donor_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    campaign_id: Mapped[int] = mapped_column(ForeignKey("campaigns.id"), nullable=False)
    item_id: Mapped[int | None] = mapped_column(ForeignKey("items.id"), nullable=True)

    donation_type: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default=DonationStatus.PENDING.value, nullable=False)

    quantity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    amount: Mapped[float | None] = mapped_column(Float, nullable=True)

    donor_note: Mapped[str | None] = mapped_column(Text, nullable=True)
    admin_note: Mapped[str | None] = mapped_column(Text, nullable=True)

    recommendation_level: Mapped[str | None] = mapped_column(String(50), nullable=True)
    recommendation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    better_alternative: Mapped[str | None] = mapped_column(String(120), nullable=True)
    suggested_quantity: Mapped[int | None] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    received_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    used_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    donor = relationship("User", back_populates="donations")
    campaign = relationship("Campaign", back_populates="donations")
    item = relationship("Item", back_populates="donations")