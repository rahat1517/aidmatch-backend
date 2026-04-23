from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.campaigns import router as campaign_router
from app.api.v1.items import router as item_router
from app.api.v1.donations import router as donation_router
from app.api.v1.recommendations import router as recommendation_router
from app.api.v1.notifications import router as notification_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(campaign_router)
api_router.include_router(item_router)
api_router.include_router(donation_router)
api_router.include_router(recommendation_router)
api_router.include_router(notification_router)