# connectors/binance.py
# import requests, time, Dict, Tuple, Optional, baseExchangeConnector

import requests
import time
from typing import Dict, List, Tuple, Optional
from .base_connector import baseExchangeConnector

# class BinanceConnector(BaseExchangeConnector)
# define __init__
class BinanceConnector(baseExchangeConnector):
    def __init__(self, api_key: str = None, api_secret: str = None):
        self.base_url = "https://api.binance.com"
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = self._init_session()

    # define _init_session
    def _init_session(self):
        session = requests.Session()
        if self.api_key:
            session.headers.update({'X-MBX-APIKEY': self.api_key})
        return session

    #define get_best_bid_ask
    def get_best_bid_ask(self, pair: str) -> Tuple[float, float]:
        url = f"/api/v3/ticker/bookTicker"
        params = {'symbol': pair}
        response = self.session.get(url, params=params).json()
        return float(response['bidPrice']), float(response['askPrice'])

    #define get_l2_order_book
    def get_l2_order_book(self, pair: str, depth: int = 100) -> Dict:
        url = f"/api/v3/depth"
        params = {'symbol': pair}
        response = self.session.get(url, params=params).json()
        return {
            'current_rate': float(response['lastFundingRate']),
            'next_funding_time': response['nextFundingTime'],
            'predicted_rate': float(response.get('nextFundingRate', 0))
        }
