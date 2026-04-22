from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from pydantic import BaseModel


class TransactionResult(BaseModel):
    """交易结果模型"""
    success: bool
    tx_hash: Optional[str] = None
    error_message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


class BlockchainAdapter(ABC):
    """区块链适配器抽象基类"""
    
    @abstractmethod
    def connect(self) -> bool:
        """连接到区块链网络"""
        pass
    
    @abstractmethod
    def send_transaction(self, transaction_data: Dict[str, Any]) -> TransactionResult:
        """发送交易到区块链"""
        pass
    
    @abstractmethod
    def get_balance(self, address: str) -> float:
        """获取账户余额"""
        pass
    
    @abstractmethod
    def get_block_info(self, block_number: int) -> Dict[str, Any]:
        """获取区块信息"""
        pass
    
    @abstractmethod
    def verify_transaction(self, tx_hash: str) -> bool:
        """验证交易是否已确认"""
        pass