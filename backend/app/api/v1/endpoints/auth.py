from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.api.deps import get_db
from app.core.security import verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Senha inválida")

    access_token = create_access_token({"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }