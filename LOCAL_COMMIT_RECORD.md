# 本地提交说明

由于网络连接问题无法推送至远程仓库，以下是在本地完成的提交记录：

## 提交历史

1. feat(models): migrate user models to SQLModel with proper foreign key relations
2. feat(schemas): update schemas to match SQLModel database relations  
3. feat(database): configure SQLModel engine with foreign key constraints
4. feat(governance): add governance service with voting logic and statistics
5. feat(routes): add votes router with SQLModel integration
6. feat(routes): update users router for SQLModel compatibility with enhanced user functions
7. feat(routes): update proposals router for SQLModel compatibility
8. feat(main): register votes router and maintain API structure
9. feat(init): update db initialization for SQLModel compatibility

## 文件更改状态

所有更改文件：
- backend/app/models.py
- backend/app/schemas.py
- backend/app/database.py
- backend/app/main.py
- backend/app/routers/users.py
- backend/app/routers/proposals.py
- backend/app/routers/votes.py
- backend/app/services/governance_service.py
- backend/init_db.py

新增文件：
- backend/app/routers/votes.py
- backend/app/services/governance_service.py

## 核心功能完成

用户注册功能已完全部署在本地，位于 /api/v1/users/ endpoint。