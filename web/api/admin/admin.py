# web/admin/admin.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from web.api.auth import models, security
from web.api.db.database import get_db
from web.api.db import models as db_models

router = APIRouter()

def get_current_admin_user(db: Session = Depends(get_db), token: str = Depends(security.oauth2_scheme)):
    """
    获取当前登录的管理员用户
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = security.decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    user = db.query(db_models.User).filter(db_models.User.username == username).first()
    if user is None or user.id != 1:  # 默认第一个注册的是管理员
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    return user

@router.get("/check", response_model=dict)
def check_admin(db: Session = Depends(get_db), current_user: db_models.User = Depends(get_current_admin_user)):
    """
    检查当前用户是否为管理员
    """
    if current_user.id == 1:  # 默认第一个注册的是管理员
        return {"isAdmin": True}
    else:
        return {"isAdmin": False}

@router.get("/users", response_model=List[models.UserResponse])
def list_users(db: Session = Depends(get_db), current_user: db_models.User = Depends(get_current_admin_user)):
    """
    获取所有用户信息
    """
    users = db.query(db_models.User).all()
    return users

@router.post("/users", response_model=models.UserResponse)
def create_user(user: models.UserCreate, db: Session = Depends(get_db), current_user: db_models.User = Depends(get_current_admin_user)):
    """
    创建新用户
    """
    existing_user = db.query(db_models.User).filter(db_models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    hashed_password = security.get_password_hash(user.password)
    new_user = db_models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        disabled=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.delete("/users/{user_id}", response_model=models.UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: db_models.User = Depends(get_current_admin_user)):
    """
    删除用户
    """
    user = db.query(db_models.User).filter(db_models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db.delete(user)
    db.commit()
    return user

@router.put("/users/{user_id}/disable", response_model=models.UserResponse)
def disable_user(user_id: int, db: Session = Depends(get_db), current_user: db_models.User = Depends(get_current_admin_user)):
    """
    禁用用户
    """
    user = db.query(db_models.User).filter(db_models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user.disabled = True
    db.commit()
    db.refresh(user)
    return user

@router.put("/users/{user_id}/enable", response_model=models.UserResponse)
def enable_user(user_id: int, db: Session = Depends(get_db), current_user: db_models.User = Depends(get_current_admin_user)):
    """
    启用用户
    """
    user = db.query(db_models.User).filter(db_models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user.disabled = False
    db.commit()
    db.refresh(user)
    return user
