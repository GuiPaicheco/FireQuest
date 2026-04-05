from fastapi import APIRouter
from app.api.v1.endpoints import user, auth
from app.api.v1.endpoints import mission

api_router = APIRouter()

api_router.include_router(mission.router, prefix="/missions", tags=["Missions"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])