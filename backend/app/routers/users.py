# File: backend/app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid
from typing import List, Optional

# 引入数据库会话和模型
from ..database import SessionLocal, engine
from .. import models

# 创建数据库表（如果还没创建）
models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# --- 依赖项：获取数据库会话 ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Pydantic 模型 (数据验证) ---
class UserCreate(BaseModel):
    username: str
    # 初始余额可选，默认 1000
    mock_token_balance: float = 1000.0 

class UserResponse(BaseModel):
    id: int
    username: str
    mock_address: str
    mock_token_balance: float
    reputation: int

    class Config:
        from_attributes = True

# --- 接口定义 ---

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    创建一个新用户，并自动生成模拟钱包地址
    """
    # 1. 检查用户名是否存在
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")

    # 2. 生成模拟钱包地址 (模拟 0x + 40位十六进制)
    mock_address = "0x" + uuid.uuid4().hex

    # 3. 创建数据库对象
    new_user = models.User(
        username=user.username,
        mock_address=mock_address,
        mock_token_balance=user.mock_token_balance
    )

    # 4. 提交到数据库
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    获取用户列表
    """
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users 