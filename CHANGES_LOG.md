# 项目更新日志

## 已完成的更改（2026年4月18日）

### 🔧 核心功能更新

#### 1. 数据库模型重构 (SQLModel)
- `models.py`: 从SQLAlchemy模型完整迁移至SQLModel
- 添加了正确的外键关系定义
- 解决了User、Proposal、Vote之间的关联问题

#### 2. 数据验证层更新 (Pydantic)
- `schemas.py`: 更新数据验证模型以匹配新的数据库关系
- 修改Proposal和Vote使用ID而非地址作为关联键

#### 3. 数据库配置优化
- `database.py`: 更新为SQLModel引擎配置
- 启用SQLite外键约束支持

#### 4. 用户路由增强
- `routers/users.py`: 完全重构为SQLModel兼容
- 添加了用户治理统计API (`/governance_stats`)
- 更新所有数据库查询为select/exec模式

#### 5. 新增投票路由
- `routers/votes.py`: 完全新的投票管理路由
- 支持按用户、提案查询投票记录

#### 6. 治理服务模块
- `services/governance_service.py`: 提供治理相关的业务逻辑
- 包含投票统计、权重计算等功能

#### 7. 提案路由适配
- `routers/proposals.py`: 更新为SQLModel兼容
- 添加提案统计API

#### 8. 主应用注册
- `main.py`: 注册新的votes路由模块
- 维护API端点结构

#### 9. 数据库初始化
- `init_db.py`: 更新为SQLModel创建表方式

### 🚀 新增API端点

#### 用户模块 (POST /api/v1/users/)
- `/` -> 用户注册（主功能）
- `/{user_id}` -> 获取用户详情
- `/address/{address}` -> 按地址获取用户
- `/` (PUT) -> 更新用户
- `/{user_id}/governance_stats` -> 获取用户治理统计

#### 提案模块 (POST /api/v1/proposals/)
- `/` -> 创建提案
- `/` (GET) -> 获取提案列表
- `/{id}` -> 获取提案详情
- `/{id}` (PUT) -> 更新提案
- `/` (DELETE) -> 删除提案
- `/{id}/stats` -> 获取提案统计

#### 投票模块 (POST /api/v1/votes/)
- `/` -> 创建投票
- `/` (GET) -> 获取投票列表
- `/user/{user_id}` -> 获取用户投票历史
- `/proposal/{proposal_id}` -> 获取提案投票详情

### 🔐 核心特性

1. **完整用户注册流程**: 自动分配模拟钱包地址
2. **数据验证**: 请求/响应数据完整验证
3. **数据库关系**: 正确的外键关联和层级结构
4. **错误处理**: 完善的HTTP异常响应
5. **治理统计**: 用户和提案参与度统计数据

---

**重要**: 所有更改已完成，但由于网络连接问题未能推送到远程仓库。所有功能已本地测试通过。