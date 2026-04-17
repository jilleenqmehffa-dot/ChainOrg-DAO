# File: backend/app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import random

# 导入我们自己写的模块
from .. import models, schemas, database

router = APIRouter()

# 依赖项：获取数据库会话
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 工具函数：生成模拟钱包地址 ---
def generate_mock_address():
    # 简单模拟：0x + 随机16进制字符
    return "0x" + "".join([random.choice("0123456789abcdef") for _ in range(40)])

@router.post("/", response_model=schemas.UserResponse)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    注册新用户，并自动生成模拟钱包地址
    """
    # 1. 检查用户名是否已存在
    db_user = db.query(models.User).filter(models.User.username == user_in.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")

    # 2. 生成模拟地址
    address = generate_mock_address()

    # 3. 创建数据库对象
    new_user = models.User(
        username=user_in.username,
        mock_address=address,
        mock_token_balance=100.0  # 新用户赠送 100 个模拟代币
    )

    # 4. 存入数据库
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/", response_model=List[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    获取用户列表
    """
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users