# File: backend/app/services/governance_service.py

from sqlmodel import Session, select
from .. import models
from typing import Optional

class GovernanceService:
    """
    处理DAO治理相关业务逻辑的服务类
    """
    
    @staticmethod
    def get_user_by_address(db: Session, address: str) -> Optional[models.User]:
        """根据地址查询用户"""
        statement = select(models.User).where(models.User.mock_address == address)
        user = db.exec(statement).first()
        return user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
        """根据ID查询用户"""
        statement = select(models.User).where(models.User.id == user_id)
        user = db.exec(statement).first()
        return user
    
    @staticmethod
    def get_proposal_stats(db: Session, proposal_id: int) -> dict:
        """获取提案统计信息（赞成/反对票数）"""
        # 先获取提案
        proposal = db.get(models.Proposal, proposal_id)
        if not proposal:
            return {}
        
        # 直接计算投票统计
        yes_count_statement = select(models.Vote).where(
            models.Vote.proposal_id == proposal_id,
            models.Vote.vote_option == True
        )
        no_count_statement = select(models.Vote).where(
            models.Vote.proposal_id == proposal_id,
            models.Vote.vote_option == False
        )
        total_statement = select(models.Vote).where(models.Vote.proposal_id == proposal_id)
        
        yes_count = len(db.exec(yes_count_statement).all())
        no_count = len(db.exec(no_count_statement).all())
        total_count = len(db.exec(total_statement).all())
        
        return {
            "total_votes": total_count,
            "yes_votes": yes_count,
            "no_votes": no_count,
            "proposal_status": proposal.status
        }
    
    @staticmethod
    def calculate_voting_power(db: Session, user_id: int) -> float:
        """计算用户投票权"""
        user = GovernanceService.get_user_by_id(db, user_id)
        if not user:
            return 0.0
        return user.mock_token_balance  # 以代币余额作为投票权重
   
    @staticmethod
    def check_proposal_eligible_for_execution(db: Session, proposal_id: int) -> bool:
        """检查提案是否有资格执行"""
        stats = GovernanceService.get_proposal_stats(db, proposal_id)
        if not stats:
            return False
        
        # 基本规则：需要超过50%的赞成票才可通过
        if stats['total_votes'] > 0 and stats['yes_votes'] > stats['total_votes'] / 2:
            return True
        return False