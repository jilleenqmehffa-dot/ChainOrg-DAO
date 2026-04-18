# File: backend/app/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- 用户相关的模型 ---

class UserCreate(BaseModel):
    """创建用户时需要的字段"""
    username: str

class UserUpdate(BaseModel):
    """用户信息更新时需要的字段"""
    username: Optional[str] = None
    mock_token_balance: Optional[float] = None

class UserResponse(BaseModel):
    """返回给前端的用户信息"""
    id: int
    username: str
    mock_address: str
    mock_token_balance: float
    reputation: int
    created_at: datetime

    class Config:
        from_attributes = True  # 关键：允许从 SQLAlchemy 模型读取数据


# --- 提案相关的模型 ---

class ProposalCreate(BaseModel):
    """创建提案时需要的字段"""
    title: str
    content: str
    creator_id: int  # 修改：使用creator_id而不是creator_address
    end_time: Optional[datetime] = None

class ProposalUpdate(BaseModel):
    """更新提案状态时需要的字段"""
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None
    end_time: Optional[datetime] = None

class ProposalResponse(BaseModel):
    """返回给前端的提案信息"""
    id: int
    title: str
    content: str
    status: str
    creator_id: int  # 修改：使用creator_id而不是creator_address
    end_time: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# --- 投票相关的模型 ---

class VoteCreate(BaseModel):
    """创建投票时需要的字段"""
    user_id: int  # 修改：使用user_id而不是user_address
    proposal_id: int
    vote_option: bool  # True为赞成，False为反对

class VoteResponse(BaseModel):
    """返回给前端的投票信息"""
    id: int
    user_id: int  # 修改：使用user_id而不是user_address
    proposal_id: int
    vote_option: bool
    weight: float
    voted_at: datetime

    class Config:
        from_attributes = True


# --- 交易相关的模型 ---

class TransactionCreate(BaseModel):
    """创建交易时需要的字段"""
    from_address: str
    to_address: str
    value: float
    proposal_id: Optional[int] = None

class TransactionUpdate(BaseModel):
    """更新交易状态时需要的字段"""
    status: Optional[str] = None

class TransactionResponse(BaseModel):
    """返回给前端的交易信息"""
    id: int
    tx_hash: str
    from_address: str
    to_address: str
    value: float
    block_number: int
    status: str
    proposal_id: Optional[int] = None
    timestamp: datetime

    class Config:
        from_attributes = True