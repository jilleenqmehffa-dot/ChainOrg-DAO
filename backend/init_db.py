# File: backend/init_db.py
from app.database import engine, Base
from app import models  # 必须导入 models，否则 Base 不知道要创建哪些表

print("正在创建数据库表...")
Base.metadata.create_all(bind=engine)
print("数据库初始化完成！请检查当前目录是否生成了 chainorg.db")