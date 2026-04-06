from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.api.deps import get_db, get_current_user
from app.core.security import hash_password
from sqlalchemy.exc import IntegrityError
from app.core.response import success_response

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    from sqlalchemy.exc import IntegrityError

    db.add(db_user)

    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Usuário ou email já existe")
    return db_user

@router.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    return success_response({
        "id": current_user.id,
        "username": current_user.username,
        "xp": current_user.xp
    })

@router.get("/ranking")
def get_ranking(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.xp.desc()).all()

    ranking = []

    position = 1
    for user in users:
        ranking.append({
            "position": position,
            "username": user.username,
            "xp": user.xp
        })
        position += 1

    return success_response(ranking)