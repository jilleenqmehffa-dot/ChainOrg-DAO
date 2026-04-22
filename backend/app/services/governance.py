# File: backend/app/services/governance.py

from typing import Dict, Any, Optional
from sqlmodel import Session
from ..adapters.base import BlockchainAdapter, TransactionResult
from ..adapters.mock_chain import MockBlockchainAdapter


class GovernanceService:
    """
    治理服务类，用于封装与治理相关的业务逻辑
    包括提案、投票等与区块链交互的功能
    """
    
    def __init__(self, blockchain_adapter: Optional[BlockchainAdapter] = None):
        """
        初始化治理服务
        :param blockchain_adapter: 区块链适配器实例，默认使用模拟适配器
        """
        self.blockchain_adapter = blockchain_adapter or MockBlockchainAdapter()
        if not self.blockchain_adapter.connect():
            raise Exception("无法连接到区块链网络")
    
    def submit_proposal_on_chain(self, proposal_data: Dict[str, Any]) -> TransactionResult:
        """
        将提案提交到区块链
        :param proposal_data: 包含提案详细信息的数据字典
        :return: 交易结果
        """
        transaction_data = {
            "from": proposal_data.get("creator_address"),
            "to": proposal_data.get("dao_contract_address", "0xDAO_CONTRACT"),
            "value": 0,  # DAO提案通常不需要支付费用
            "data": {
                "method": "submitProposal",
                "args": [
                    proposal_data.get("title"),
                    proposal_data.get("description"),
                    proposal_data.get("voting_duration", 7)
                ]
            }
        }
        
        result = self.blockchain_adapter.send_transaction(transaction_data)
        return result
    
    def cast_vote_on_chain(self, vote_data: Dict[str, Any]) -> TransactionResult:
        """
        链上投票
        :param vote_data: 包含投票信息的数据字典
        :return: 交易结果
        """
        transaction_data = {
            "from": vote_data.get("voter_address"),
            "to": vote_data.get("dao_contract_address", "0xDAO_CONTRACT"),
            "value": 0,  # 投票通常不需要支付费用
            "data": {
                "method": "castVote",
                "args": [
                    vote_data.get("proposal_id"),
                    vote_data.get("vote_option"),  # true for yes, false for no
                    vote_data.get("voting_power", 1)
                ]
            }
        }
        
        result = self.blockchain_adapter.send_transaction(transaction_data)
        return result
    
    def execute_proposal_on_chain(self, proposal_id: int) -> TransactionResult:
        """
        执行已通过的提案
        :param proposal_id: 提案ID
        :return: 交易结果
        """
        transaction_data = {
            "from": "0xDAO_EXECUTOR",  # 执行者地址
            "to": "0xDAO_CONTRACT",
            "value": 0,
            "data": {
                "method": "executeProposal",
                "args": [proposal_id]
            }
        }
        
        result = self.blockchain_adapter.send_transaction(transaction_data)
        return result
    
    def get_voter_balance(self, voter_address: str) -> float:
        """
        获取投票者的余额（可以用作投票权重）
        :param voter_address: 投票者地址
        :return: 余额数量
        """
        return self.blockchain_adapter.get_balance(voter_address)
    
    def verify_transaction_status(self, tx_hash: str) -> bool:
        """
        验证交易状态
        :param tx_hash: 交易哈希
        :return: 交易是否已确认
        """
        return self.blockchain_adapter.verify_transaction(tx_hash)


# 一个便捷函数来获取治理服务实例
def get_governance_service() -> GovernanceService:
    """
    获取默认的治理服务实例
    使用模拟区块链适配器
    """
    return GovernanceService()