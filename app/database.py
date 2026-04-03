# File: backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 1. 配置 SQLite 数据库文件路径
# 这会在当前目录自动生成一个 chainorg.db 文件
DATABASE_URL = "sqlite:///./chainorg.db"

# 2. 创建引擎
# echo=True 可以在终端看到生成的SQL语句，调试时很有用
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)

# 3. 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 基类（上面的 models.py 会用到这个 Base）
Base = declarative_base()