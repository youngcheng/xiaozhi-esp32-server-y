# web/auth/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from web.api.auth import models, security
from web.api.db.database import get_db
from web.api.db import models as db_models

router = APIRouter()

@router.post("/register", response_model=models.UserResponse)
def register(user: models.UserCreate, db: Session = Depends(get_db)):
    """
    用户注册接口
    检查用户名是否存在，若不存在则对密码进行 bcrypt 哈希处理后保存到数据库
    """
    # 检查用户名是否已存在
    existing_user = db.query(db_models.User).filter(db_models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    # 对密码进行 bcrypt 哈希处理
    hashed_password = security.get_password_hash(user.password)
    # 创建新用户记录
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

@router.post("/login", response_model=models.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    用户登录接口
    通过 OAuth2PasswordRequestForm 获取表单中的 username 和 password，
    查询数据库，验证密码后生成 JWT 令牌返回
    """
    # 从数据库中查询用户
    user = db.query(db_models.User).filter(db_models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
