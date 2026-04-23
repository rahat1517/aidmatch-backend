from fastapi import FastAPI

from app.core.config import settings
from app.core.database import Base, engine
from app.core.firebase import init_firebase
from app.api.v1.api import api_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)


@app.on_event("startup")
def on_startup():
    init_firebase()


@app.get("/")
def root():
    return {
        "message": "AidMatch API running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


app.include_router(api_router, prefix=settings.API_V1_STR)