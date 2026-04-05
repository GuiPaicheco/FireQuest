from fastapi import FastAPI
from app.api.v1.api import api_router
from app.db.session import engine
from app.db.base import Base

# 👇 IMPORTANTE (carrega os models)
from app.models import user, mission

app = FastAPI(title="FireQuest API")

Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api/v1")