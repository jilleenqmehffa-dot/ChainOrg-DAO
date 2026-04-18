# File: backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users, proposals, explorer, votes

# 1. 创建 FastAPI 实例
app = FastAPI(
    title="ChainOrg-DAO API",
    description="基于模拟区块链架构的去中心化自治组织后端",
    version="1.0.0"
)

# 2. 配置跨域 (CORS)
# 允许前端 (React) 访问后端接口
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 开发环境允许所有来源，生产环境需指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. 注册路由
# 这里把我们写好的接口挂载到 API 上
app.include_router(users.router, prefix="/api/v1/users", tags=["用户模块"])
app.include_router(proposals.router, prefix="/api/v1/proposals", tags=["提案模块"])
app.include_router(votes.router, prefix="/api/v1/votes", tags=["投票模块"])
app.include_router(explorer.router, prefix="/api/v1/explorer", tags=["区块链浏览器模拟"])

# 4. 根路径测试
@app.get("/")
def read_root():
    return {
        "message": "欢迎来到 ChainOrg-DAO 后端",
        "docs": "/docs" # FastAPI 自带的文档地址
    } 