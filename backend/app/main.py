from fastapi import FastAPI
from app.api.v1.api import api_router
from app.db.session import engine
from app.db.base import Base
from app.models import goal
from app.core.exception_handler import global_exception_handler
from app.models import user, mission
from fastapi.middleware.cors import CORSMiddleware
    
app = FastAPI(title="FireQuest API")

Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api/v1")

app.add_exception_handler(Exception, global_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)