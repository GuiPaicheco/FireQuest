from app.db.session import SessionLocal
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from app.core.config import settings


# 🔗 Conexão com banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔐 Usuário autenticado
def get_current_user(token: str = Depends(lambda: None)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")