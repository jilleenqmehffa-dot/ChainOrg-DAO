# File: backend/init_db.py
from app.database import engine
from app import models
from sqlmodel import SQLModel

print("正在创建数据库表...")
try:
    SQLModel.metadata.create_all(bind=engine)
    print("数据库初始化完成！请检查当前目录是否生成了 chainorg.db")
except Exception as e:
    print(f"创建数据库表时出现错误: {e}")