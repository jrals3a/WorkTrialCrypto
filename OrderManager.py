# core/order_manager.py
# import Dict, List, baseExchangeConnector

from typing import Dict, List
import baseExchangeConnector

# define class OrderManager
# define __init__
class OrderManager:
    def __init__(self, connectors: Dict[str, baseExchangeConnector]):
        self.connectors = connectors
        self.active_orders = {}

    # define place_order
    def place_order(self, exchange: str, pair: str, side: str, order_type: str, quantity: float, price: float = None) -> str:
        """Place order on specified exchange"""
        connector = self.connectors.get(exchange)
        if not connector:
            raise valueError(f"Exchange {exchange} not supported")

        order_id = connector.place_order(pair, side, order_type, quantity, price)
        self.active_orders[order_id] = {
            'exchange': exchange,
            'pair': pair,
            'side': side,
            'type': order_type,
            'quantity': quantity,
            'price': price,
            'timestamp': time.time()
        }
        return order_id

    # define cancel_order
    def cancel_order(self, order_id: str) -> bool:
        """Cancel order by order_id"""
        if order_id not in self.active_orders:
            return False
        
        order_info = self.active_orders[order_id]
        connector = self.connectors[order_info['exchange']]
        success = connector.cancel_order(order_id)

        if success:
            del self.active_orders[order_id]
        return success

    #define get_order_status
    def get_order_status(self, order_id: str) -> Dict:
        """Get order status by order_id"""
        if order_id not in self.active_orders:
            return {'status': 'UNKNOWN'}

        order_info = self.active_orders[order.id]
        connector = self.connectors[order_info['exchange']]
        return connector.get_order_status(order_id)

    # define performance_test
    def performance_test(self, exchange: str, pair: str) -> Dict:
        """Run performance test placing and canceling orders"""
        results = {
            'placement_success': 0,
            'placement_failures': 0,
            'cancel_success': 0,
            'cancel_failures': 0,
            'placement_latencies': [],
            'cancel_latencies': []
        }

        connector = self.connectors.get(exchange)
        if not connector:
            raise ValueError(f"Exchange not supported")

        for i in range(200):
            order_type = 'LIMIT' if i % 2 == 0 else 'MARKET'
            side = 'BUY' if i % 3 == 0 else 'SELL'
            quantity = 0.1
            price = None if order_type == 'MARKET' else 100.0

            try:
                start_time = time.time()
                order_id = self.place_order(exchange, pair, side, order_type, quantity, price)
                placement_time = time.time() - start_time

                results['placement_success'] += 1
                results['placement_latencies'].append(placement_time)

                start_time = time.time()
                cancel_success = self.cancel_order(order_id)
                cancel_time = time.time() - start_time

                if cancel_success:
                    results['cancel_success'] += 1
                else:
                    results['cancel_failures'] += 1
                results['cancel_latencies'].append(cancel_time)

            except Exception as e:
                results['placement_failures'] += 1
                print(f"Order failed: {str(e)}")

            # averages
            if results['placement_latencies']:
                results['avg_placement_latency'] = sum(results['placement_latencies']) / len(results['placement_latencies'])
            if results['cancel_latencies']:
                results['avg_cancel_latency'] = sum(results['cancel_latencies']) / len(results['cancel_latencies'])
            return results
