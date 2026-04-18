# File: backend/app/routers/proposals.py

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Optional
import uuid

# 引入数据库会话、模型和数据验证结构
from .. import models, schemas, database
from ..services.governance_service import GovernanceService

router = APIRouter()

# --- 依赖项：获取数据库会话 ---
def get_db():
    with Session(database.engine) as session:
        yield session

@router.post("/", response_model=schemas.ProposalResponse)
def create_proposal(proposal: schemas.ProposalCreate, db: Session = Depends(get_db)):
    """
    创建一个新的提案
    """
    # 检查用户是否存在 (使用user_id)
    user = db.get(models.User, proposal.creator_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 创建数据库对象
    new_proposal = models.Proposal(
        title=proposal.title,
        content=proposal.content,
        creator_id=proposal.creator_id,  # 修改：使用creator_id
        end_time=proposal.end_time
    )

    # 提交到数据库
    db.add(new_proposal)
    db.commit()
    db.refresh(new_proposal)

    return new_proposal

@router.get("/", response_model=List[schemas.ProposalResponse])
def get_proposals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    获取提案列表
    """
    statement = select(models.Proposal).offset(skip).limit(limit)
    proposals = db.exec(statement).all()
    return proposals

@router.get("/{proposal_id}", response_model=schemas.ProposalResponse)
def read_proposal(proposal_id: int, db: Session = Depends(get_db)):
    """
    根据ID获取单个提案详情
    """
    proposal = db.get(models.Proposal, proposal_id)
    if proposal is None:
        raise HTTPException(status_code=404, detail="提案不存在")
    return proposal

@router.put("/{proposal_id}", response_model=schemas.ProposalResponse)
def update_proposal(proposal_id: int, proposal_update: schemas.ProposalUpdate, db: Session = Depends(get_db)):
    """
    更新提案信息
    """
    proposal = db.get(models.Proposal, proposal_id)
    if proposal is None:
        raise HTTPException(status_code=404, detail="提案不存在")
    
    # 更新属性
    for field, value in proposal_update.dict(exclude_unset=True).items():
        setattr(proposal, field, value)
    
    db.add(proposal)
    db.commit()
    db.refresh(proposal)
    return proposal

@router.delete("/{proposal_id}")
def delete_proposal(proposal_id: int, db: Session = Depends(get_db)):
    """
    删除提案
    """
    proposal = db.get(models.Proposal, proposal_id)
    if proposal is None:
        raise HTTPException(status_code=404, detail="提案不存在")
    
    db.delete(proposal)
    db.commit()
    return {"message": "提案删除成功"}

@router.get("/{proposal_id}/stats", response_model=dict)
def get_proposal_stats(proposal_id: int, db: Session = Depends(get_db)):
    """
    获取提案详细统计信息
    """
    return GovernanceService.get_proposal_stats(db, proposal_id)