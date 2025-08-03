# connectors/base_connector.py
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional

class BaseExchangeConnector(ABC):
    """Abstract base class for all exchange connectors"""

    @abstractmethod
    def get_best_bid_ask(self, pair: str) -> Tuple[float, float]:
        """Get current best bid and ask prices"""
        pass

    @abstractmethod
    def get_12_order_book(self, pair: str, depth: int = 100) -> Dict:
        """Get full depth order book"""
        pass