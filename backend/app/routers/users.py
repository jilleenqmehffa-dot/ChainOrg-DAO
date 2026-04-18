# File: backend/app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from ..services.governance_service import GovernanceService
import random

# 导入我们自己写的模块
from .. import models, schemas, database

router = APIRouter()

# 依赖项：获取数据库会话
def get_db():
    with Session(database.engine) as session:  # SQLModel的会话管理方式
        yield session

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
    statement = select(models.User).where(models.User.username == user_in.username)
    db_user = db.exec(statement).first()
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
    statement = select(models.User).offset(skip).limit(limit)
    users = db.exec(statement).all()
    return users

@router.get("/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    根据ID获取单个用户信息
    """
    user = db.get(models.User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@router.get("/address/{mock_address}", response_model=schemas.UserResponse)
def read_user_by_address(mock_address: str, db: Session = Depends(get_db)):
    """
    根据模拟地址获取用户信息
    """
    statement = select(models.User).where(models.User.mock_address == mock_address)
    user = db.exec(statement).first()
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    """
    更新用户信息
    """
    user = db.get(models.User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 更新属性
    for field, value in user_update.dict(exclude_unset=True).items():
        if hasattr(user, field):
            setattr(user, field, value)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/{user_id}/governance_stats", response_model=dict)
def get_user_governance_stats(user_id: int, db: Session = Depends(get_db)):
    """
    获取用户治理参与情况统计
    """
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 统计该用户发起的提案数
    created_proposals_statement = select(models.Proposal).where(
        models.Proposal.creator_id == user.id
    )
    created_proposals = len(db.exec(created_proposals_statement).all())
    
    # 统计该用户的投票数
    user_votes_statement = select(models.Vote).where(
        models.Vote.user_id == user.id
    )
    user_votes = len(db.exec(user_votes_statement).all())
    
    # 计算投票权
    voting_power = GovernanceService.calculate_voting_power(db, user.id)
    
    return {
        "user_id": user.id,
        "username": user.username,
        "created_proposals_count": created_proposals,
        "votes_cast_count": user_votes,
        "voting_power": voting_power,
        "reputation": user.reputation
    }