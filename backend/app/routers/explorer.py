# File: backend/app/routers/explorer.py

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

# 为满足main.py中的导入需求，定义基本的响应模型
class TransactionResponse(BaseModel):
    id: int
    tx_hash: str
    from_address: str
    to_address: str
    value: float
    status: str
    proposal_id: Optional[int] = None
    timestamp: str

    class Config:
        from_attributes = True


@router.get("/transactions", response_model=List[TransactionResponse])
def get_transactions(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """
    获取模拟区块链上的交易列表（类似于区块链浏览器）
    """
    transactions = db.query(models.Transaction).offset(skip).limit(limit).all()
    return transactions


@router.get("/transactions/{address}", response_model=List[TransactionResponse])
def get_transactions_by_address(address: str, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """
    根据地址获取特定用户的交易列表
    """
    transactions = db.query(models.Transaction).filter(
        (models.Transaction.from_address == address) | 
        (models.Transaction.to_address == address)
    ).offset(skip).limit(limit).all()
    
    if not transactions:
        raise HTTPException(status_code=404, detail="未找到对应地址的交易记录")
    
    return transactions