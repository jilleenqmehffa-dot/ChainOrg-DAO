# File: backend/app/schemas.py
from pydantic import BaseModel
from typing import Optional

# --- 用户相关的模型 ---

class UserCreate(BaseModel):
    """创建用户时需要的字段"""
    username: str

class UserResponse(BaseModel):
    """返回给前端的用户信息"""
    id: int
    username: str
    mock_address: str
    mock_token_balance: float = 0.0

    class Config:
        orm_mode = True  # 关键：允许从 SQLAlchemy 模型读取数据