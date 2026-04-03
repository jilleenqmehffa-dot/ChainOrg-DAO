# File: backend/app/models.py

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()

# --- 1. 用户表 (模拟钱包) ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    
    # --- 模拟区块链核心字段 ---
    # 模拟钱包地址，例如：0x123...abc
    mock_address = Column(String(42), unique=True, index=True, nullable=False) 
    # 模拟代币余额，决定了投票权重
    mock_token_balance = Column(Float, default=1000.0, nullable=False) 
    # 声誉值
    reputation = Column(Integer, default=100) 
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系映射：一个用户可以创建多个提案，可以投多次票
    proposals = relationship("Proposal", back_populates="creator")
    votes = relationship("Vote", back_populates="voter")

    def __repr__(self):
        return f"<User {self.username} (Addr: {self.mock_address[:6]})>"


# --- 2. 提案表 (DAO治理核心) ---
class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    
    # --- 模拟状态机 ---
    # 草稿/投票中/已通过/已拒绝/执行中/已完成
    status = Column(String(20), default="Draft") 
    
    # 关联用户表（发起人）
    creator_address = Column(String(42), nullable=False) 
    
    # 投票时间限制（模拟链上时间锁）
    end_time = Column(DateTime, nullable=True) 
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系映射
    creator = relationship("User", back_populates="proposals")
    votes = relationship("Vote", back_populates="proposal")
    transactions = relationship("Transaction", back_populates="related_proposal")

    def __repr__(self):
        return f"<Proposal {self.id}: {self.title}>"


# --- 3. 投票记录表 ---
class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    
    # 关联投票人地址
    user_address = Column(String(42), nullable=False) 
    # 关联提案ID
    proposal_id = Column(Integer, ForeignKey("proposals.id"), nullable=False) 
    
    # 赞成(True) 或 反对(False)
    vote_option = Column(Boolean, nullable=False) 
    # 投票时的权重（快照）
    weight = Column(Float, nullable=False) 
    
    voted_at = Column(DateTime, default=datetime.utcnow)

    # 关系映射
    proposal = relationship("Proposal", back_populates="votes")
    voter = relationship("User", back_populates="votes")


# --- 4. 交易流水表 (模拟区块链浏览器数据) ---
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    
    # --- 模拟链上交易核心 ---
    # 模拟交易Hash
    tx_hash = Column(String(66), unique=True, index=True, default=lambda: '0x' + str(uuid.uuid4().hex)) 
    # 发送方
    from_address = Column(String(42), nullable=False) 
    # 接收方
    to_address = Column(String(42), nullable=False) 
    # 转账金额
    value = Column(Float, nullable=False) 
    
    # --- 模拟区块信息 ---
    block_number = Column(Integer, default=0) 
    # 状态：Pending, Confirmed, Failed
    status = Column(String(20), default="Pending") 
    
    # 关联DAO提案（证明是哪笔提案触发的）
    proposal_id = Column(Integer, ForeignKey("proposals.id"), nullable=True) 
    
    timestamp = Column(DateTime, default=datetime.utcnow)

    # 关系映射
    related_proposal = relationship("Proposal", back_populates="transactions")

    def __repr__(self):
        return f"<Tx {self.tx_hash[:8]}: {self.value} ETH>"