# File: backend/app/routers/proposals.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

# 引入数据库会话和模型
from ..database import SessionLocal, engine
from .. import models

router = APIRouter()

# --- 依赖项：获取数据库会话 ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 为了满足main.py中的导入需求，这里也创建一个基本的提案模型
# 需要定义Pydantic模型
class ProposalCreate(BaseModel):
    title: str
    content: str
    creator_address: str

class ProposalResponse(BaseModel):
    id: int
    title: str
    content: str
    creator_address: str
    status: str
    end_time: Optional[str] = None

    class Config:
        from_attributes = True


@router.post("/", response_model=ProposalResponse)
def create_proposal(proposal: ProposalCreate, db: Session = Depends(get_db)):
    """
    创建一个新的提案
    """
    # 检查用户是否存在
    user = db.query(models.User).filter(models.User.mock_address == proposal.creator_address).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 创建数据库对象
    new_proposal = models.Proposal(
        title=proposal.title,
        content=proposal.content,
        creator_address=proposal.creator_address
    )

    # 提交到数据库
    db.add(new_proposal)
    db.commit()
    db.refresh(new_proposal)

    return new_proposal


@router.get("/", response_model=List[ProposalResponse])
def get_proposals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    获取提案列表
    """
    proposals = db.query(models.Proposal).offset(skip).limit(limit).all()
    return proposals