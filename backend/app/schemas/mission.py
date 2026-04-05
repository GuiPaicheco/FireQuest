from pydantic import BaseModel
from datetime import datetime

class MissionCreate(BaseModel):
    title: str
    description: str
    difficulty: int
    urgency: int
    due_date: datetime | None = None

class MissionResponse(BaseModel):
    id: int
    title: str
    description: str
    difficulty: int
    urgency: int
    xp: int
    completed: bool

    class Config:
        from_attributes = True