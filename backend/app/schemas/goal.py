from pydantic import BaseModel


class GoalCreate(BaseModel):
    title: str
    description: str
    is_daily: bool = False


class GoalResponse(BaseModel):
    id: int
    title: str
    description: str
    is_daily: bool
    is_completed: bool

    class Config:
        from_attributes = True