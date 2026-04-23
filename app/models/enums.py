import enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    DONOR = "donor"


class DonationType(str, enum.Enum):
    CASH = "cash"
    ITEM = "item"
    KIT = "kit"


class DonationStatus(str, enum.Enum):
    PENDING = "pending"
    RECEIVED = "received"
    USED = "used"
    REJECTED = "rejected"