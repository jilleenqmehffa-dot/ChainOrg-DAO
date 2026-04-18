# File: backend/app/models.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid
from sqlalchemy import Column, String as SQLString, Float as SQLFloat, Text as SQLText, DateTime as SQLDateTime, Boolean as SQLBoolean, Integer as SQLInteger

# 定义所有模型基类
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column(SQLString(50), unique=True, index=True, nullable=False))
    
    # 模拟区块链核心字段
    mock_address: str = Field(sa_column=Column(SQLString(42), unique=True, index=True, nullable=False))
    mock_token_balance: float = Field(sa_column=Column(SQLFloat, default=1000.0, nullable=False))
    reputation: int = Field(sa_column=Column(SQLInteger, default=100))
    
    created_at: Optional[datetime] = Field(sa_column=Column(SQLDateTime, default=datetime.utcnow))

    # 关系映射：一个用户可以创建多个提案，可以投多次票
    proposals: List["Proposal"] = Relationship(back_populates="creator", sa_relationship_kwargs={"lazy": "select"})
    votes: List["Vote"] = Relationship(back_populates="voter", sa_relationship_kwargs={"lazy": "select"})


class Proposal(SQLModel, table=True):
    __tablename__ = "proposals"

    id: int = Field(default=None, primary_key=True)
    title: str = Field(sa_column=Column(SQLString(200), nullable=False))
    content: Optional[str] = Field(sa_column=Column(SQLText))
    
    # 模拟状态机
    status: str = Field(sa_column=Column(SQLString(20), default="Draft")) 
    
    # 关联用户ID（发起人）
    creator_id: int = Field(foreign_key="users.id")
    
    # 投票时间限制（模拟链上时间锁）
    end_time: Optional[datetime] = Field(sa_column=Column(SQLDateTime, nullable=True))
    
    created_at: Optional[datetime] = Field(sa_column=Column(SQLDateTime, default=datetime.utcnow))

    # 关系映射
    creator: Optional[User] = Relationship(back_populates="proposals", sa_relationship_kwargs={"lazy": "select"})
    votes: List["Vote"] = Relationship(back_populates="proposal", sa_relationship_kwargs={"lazy": "select"})
    transactions: List["Transaction"] = Relationship(back_populates="related_proposal", sa_relationship_kwargs={"lazy": "select"})


class Vote(SQLModel, table=True):
    __tablename__ = "votes"

    id: int = Field(default=None, primary_key=True)
    
    # 关联投票人ID
    user_id: int = Field(foreign_key="users.id")
    # 关联提案ID
    proposal_id: int = Field(foreign_key="proposals.id")
    
    # 赞成(True) 或 反对(False)  
    vote_option: bool = Field(sa_column=Column(SQLBoolean, nullable=False))
    # 投票时的权重（快照）
    weight: float = Field(sa_column=Column(SQLFloat, nullable=False))
    
    voted_at: Optional[datetime] = Field(sa_column=Column(SQLDateTime, default=datetime.utcnow))

    # 关系映射
    proposal: Optional[Proposal] = Relationship(back_populates="votes", sa_relationship_kwargs={"lazy": "select"})
    voter: Optional[User] = Relationship(back_populates="votes", sa_relationship_kwargs={"lazy": "select"})


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"

    id: int = Field(default=None, primary_key=True)
    
    # 模拟链上交易核心
    tx_hash: str = Field(default_factory=lambda: '0x' + str(uuid.uuid4().hex), sa_column=Column(SQLString(66), unique=True, index=True))
    from_address: str = Field(sa_column=Column(SQLString(42), nullable=False))
    to_address: str = Field(sa_column=Column(SQLString(42), nullable=False))
    value: float = Field(sa_column=Column(SQLFloat, nullable=False))
    
    # 模拟区块信息
    block_number: int = Field(sa_column=Column(SQLInteger, default=0))
    status: str = Field(sa_column=Column(SQLString(20), default="Pending"))
    
    # 关联DAO提案（证明是哪笔提案触发的）
    proposal_id: Optional[int] = Field(default=None, foreign_key="proposals.id")
    
    timestamp: Optional[datetime] = Field(sa_column=Column(SQLDateTime, default=datetime.utcnow))

    # 关系映射
    related_proposal: Optional[Proposal] = Relationship(back_populates="transactions", sa_relationship_kwargs={"lazy": "select"})