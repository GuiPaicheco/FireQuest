from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.goal import GoalCreate, GoalResponse
from app.models.goal import Goal
from app.models.user import User
from app.api.deps import get_db, get_current_user

router = APIRouter()


@router.post("/", response_model=GoalResponse)
def create_goal(
    goal: GoalCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.username == current_user).first()

    db_goal = Goal(
        title=goal.title,
        description=goal.description,
        is_daily=goal.is_daily,
        owner_id=user.id
    )

    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)

    return db_goal