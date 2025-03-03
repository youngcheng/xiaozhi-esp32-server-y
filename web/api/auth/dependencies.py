# web/auth/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from web.api.auth import security
from web.api.db.database import get_db
from web.api.db import models as db_models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_user(db: Session, username: str):
    """
    获取用户（从数据库中查询）
    """
    return db.query(db_models.User).filter(db_models.User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    """
    验证用户凭证
    使用数据库中的用户数据进行验证
    """
    user = get_user(db, username)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    从 JWT 令牌中解析用户，并从数据库中获取该用户
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(db, username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: db_models.User = Depends(get_current_user)):
    """
    检查当前用户是否处于激活状态
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
