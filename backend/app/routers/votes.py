# File: backend/app/routers/votes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

# 引入数据库会话、模型和数据验证结构
from .. import models, schemas, database
from ..services.governance_service import GovernanceService

router = APIRouter()

# --- 依赖项：获取数据库会话 ---
def get_db():
    with Session(database.engine) as session:
        yield session

# --- 投票相关接口 ---
@router.post("/", response_model=schemas.VoteResponse)
def create_vote(vote: schemas.VoteCreate, db: Session = Depends(get_db)):
    """
    创建新的投票记录
    """
    # 检查用户是否存在 (使用user_id)
    user = db.get(models.User, vote.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 检查提案是否存在
    proposal = db.get(models.Proposal, vote.proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="提案不存在")
    
    # 创建投票记录
    new_vote = models.Vote(
        user_id=vote.user_id,  # 修改：使用user_id
        proposal_id=vote.proposal_id,
        vote_option=vote.vote_option,
        weight=user.mock_token_balance  # 使用用户代币余额作为投票权重
    )
    
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)
    
    return new_vote

@router.get("/", response_model=List[schemas.VoteResponse])
def get_votes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    获取投票列表
    """
    statement = select(models.Vote).offset(skip).limit(limit)
    votes = db.exec(statement).all()
    return votes

@router.get("/{vote_id}", response_model=schemas.VoteResponse)
def read_vote(vote_id: int, db: Session = Depends(get_db)):
    """
    根据ID获取单个投票记录
    """
    vote = db.get(models.Vote, vote_id)
    if vote is None:
        raise HTTPException(status_code=404, detail="投票记录不存在")
    return vote

@router.get("/user/{user_id}", response_model=List[schemas.VoteResponse])
def read_votes_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    获取用户的所有投票记录
    """
    statement = select(models.Vote).where(models.Vote.user_id == user_id)
    votes = db.exec(statement).all()
    return votes

@router.get("/proposal/{proposal_id}", response_model=List[schemas.VoteResponse])
def read_votes_by_proposal(proposal_id: int, db: Session = Depends(get_db)):
    """
    获取提案的所有投票记录
    """
    statement = select(models.Vote).where(models.Vote.proposal_id == proposal_id)
    votes = db.exec(statement).all()
    return votes

@router.get("/{vote_id}", response_model=schemas.VoteResponse)
def read_vote(vote_id: int, db: Session = Depends(get_db)):
    """
    根据ID获取单个投票记录
    """
    vote = db.query(models.Vote).filter(models.Vote.id == vote_id).first()
    if vote is None:
        raise HTTPException(status_code=404, detail="投票记录不存在")
    return vote

@router.get("/user/{user_id}", response_model=List[schemas.VoteResponse])
def read_votes_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    获取用户的所有投票记录
    """
    votes = db.query(models.Vote).filter(models.Vote.user_id == user_id).all()
    return votes

@router.get("/proposal/{proposal_id}", response_model=List[schemas.VoteResponse])
def read_votes_by_proposal(proposal_id: int, db: Session = Depends(get_db)):
    """
    获取提案的所有投票记录
    """
    votes = db.query(models.Vote).filter(models.Vote.proposal_id == proposal_id).all()
    return votes