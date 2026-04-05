from app.db.session import SessionLocal
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer

# Banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Usuário autenticado
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")