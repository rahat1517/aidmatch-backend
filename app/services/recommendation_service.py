from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.item import Item
from app.models.campaign import Campaign


def get_recommendation(
    db: Session,
    campaign_id: int,
    donation_type: str,
    item_id: int | None = None,
    quantity: int | None = None,
    amount: float | None = None
):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    item = None
    if item_id:
        item = db.query(Item).filter(Item.id == item_id, Item.campaign_id == campaign_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found in campaign")

    if donation_type == "cash":
        return {
            "recommendation_level": "good",
            "reason": "Cash is flexible and helps admins buy the most urgent needs.",
            "better_alternative": item.name if item else None,
            "suggested_quantity": None
        }

    if donation_type == "item":
        if not item:
            raise HTTPException(status_code=400, detail="item_id is required for item donation")

        remaining_need = max(item.required_quantity - item.used_quantity, 0)

        if remaining_need == 0:
            return {
                "recommendation_level": "low",
                "reason": f"{item.name} is already sufficiently covered.",
                "better_alternative": "cash",
                "suggested_quantity": 0
            }

        if quantity is None:
            quantity = 1

        if quantity <= remaining_need:
            return {
                "recommendation_level": "high",
                "reason": f"{item.name} is still needed for this campaign.",
                "better_alternative": None,
                "suggested_quantity": quantity
            }

        return {
            "recommendation_level": "medium",
            "reason": f"Requested quantity is higher than current remaining need for {item.name}.",
            "better_alternative": "cash",
            "suggested_quantity": remaining_need
        }

    if donation_type == "kit":
        return {
            "recommendation_level": "medium",
            "reason": "Kits are useful, but specific needed items may be more efficient.",
            "better_alternative": "cash",
            "suggested_quantity": quantity
        }

    raise HTTPException(status_code=400, detail="Invalid donation type")