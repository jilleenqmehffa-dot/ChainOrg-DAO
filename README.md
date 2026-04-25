# ChainOrg-DAO

ChainOrg-DAO 是一个基于 Web3 技术的去中心化自治组织平台，该项目现在包含了前后端两个部分：

## 项目结构

- `backend/`: 后端服务，基于 FastAPI 和 SQLModel
- `frontend/`: 前端服务，基于 React 和 Vite

## 启动指南

### 后端服务

```bash
cd backend
pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --reload
```

服务将在 `http://localhost:8000` 上运行

### 前端服务

```bash
cd frontend
npm install
npm run dev
```

服务将在 `http://localhost:3000` 上运行