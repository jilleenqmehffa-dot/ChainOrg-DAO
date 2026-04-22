import random
import time
from typing import Dict, Any, Optional
from .base import BlockchainAdapter, TransactionResult


class MockBlockchainAdapter(BlockchainAdapter):
    """
    模拟区块链适配器实现 
    用于开发和测试阶段，模拟真实区块链的行为
    """
    
    def __init__(self):
        self._is_connected = False
        self._balances: Dict[str, float] = {}
        self._transactions = {}
    
    def connect(self) -> bool:
        """
        连接到模拟区块链
        实际上只是设置连接状态，在模拟环境中总是返回True
        """
        self._is_connected = True
        return True
    
    def send_transaction(self, transaction_data: Dict[str, Any]) -> TransactionResult:
        """
        发送模拟交易
        生成随机交易哈希并模拟成功或失败的情况
        """
        # 为了简单起见，假设大多数交易都会成功
        success = random.random() > 0.1  # 90% 成功率
        
        # 生成模拟的交易哈希
        tx_hash = f"0x{random.randint(10**10, 10**20):020x}{int(time.time())}"
        
        if success:
            # 模拟转账操作
            from_addr = transaction_data.get('from', '')
            to_addr = transaction_data.get('to', '')
            value = transaction_data.get('value', 0)
            
            if from_addr and self._balances.get(from_addr, 0) >= value:
                self._balances[from_addr] = self._balances.get(from_addr, 0) - value
                self._balances[to_addr] = self._balances.get(to_addr, 0) + value
                self._transactions[tx_hash] = {
                    "from": from_addr,
                    "to": to_addr,
                    "value": value,
                    "timestamp": time.time(),
                    "status": "success"
                }
                
            result = TransactionResult(
                success=True,
                tx_hash=tx_hash,
                data={"block_number": random.randint(1000000, 2000000)}
            )
        else:
            error_msg = "Network error: Could not broadcast transaction"
            result = TransactionResult(
                success=False,
                tx_hash=None,
                error_message=error_msg
            )
        
        return result
    
    def get_balance(self, address: str) -> float:
        """
        获取模拟账户余额
        如果地址不存在，则返回默认值
        """
        if address not in self._balances:
            # 模拟新账户有一个初始余额
            self._balances[address] = round(random.uniform(1, 1000), 4)
        return self._balances[address]
    
    def get_block_info(self, block_number: int) -> Dict[str, Any]:
        """
        获取模拟区块信息
        返回带有指定区块号的模拟数据
        """
        return {
            "number": block_number,
            "hash": f"0x{random.getrandbits(256):x}",
            "timestamp": int(time.time()) - random.randint(0, 300),
            "size": random.randint(1000, 50000),
            "gas_limit": 30000000,
            "gas_used": random.randint(100000, 15000000)
        }
    
    def verify_transaction(self, tx_hash: str) -> bool:
        """
        验证交易是否被确认
        在模拟环境中，检查是否存在此交易
        """
        return tx_hash in self._transactions