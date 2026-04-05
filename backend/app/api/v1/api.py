from fastapi import APIRouter
from app.api.v1.endpoints import user, auth, mission, goal

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(mission.router, prefix="/missions", tags=["Missions"])
api_router.include_router(goal.router, prefix="/goals", tags=["Goals"])