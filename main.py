# main.py
# import Binance, bitsmart, KuCoin, OrderManager, SymbolMapper, and HistoricalDataStorage

from connectors.binance import BinanceConnector
from connectors.bitmart import BitmartConnector
from connectors.kucoin import KuCoinConnector
from core.order_manager import OrderManager
from core.symbol_mapper import SymbolMapper
from data.historical_storage import HistoricalDataStorage
import time
import threading

# define main
def main():
    # Initialize connectors
    connectors = {
        'binance': BinanceConnector(api_key='YOUR_API_KEY', api_secret='YOUR_API_SECRET'),
        'bitmart': BitmartConnector(api_key='YOUR_API_KEY', api_secret='YOUR_API_SECRET'),
        'kucoin': KuCoinConnector(api_key='YOUR_API_KEY', api_secret='YOUR_API_SECRET'),
        # Add other exchanges
    }
    
    # Initialize components
    order_manager = OrderManager(connectors)
    symbol_mapper = SymbolMapper()
    storage = HistoricalDataStorage(storage_type='local')
    
    # Example usage
    universal_symbol = symbol_mapper.to_universal('binance', 'BTCUSDT')
    print(f"Universal symbol: {universal_symbol}")
    
    # Start data collection thread
    # define collect_Data
    def collect_data():
        while True:
            for exchange, connector in connectors.items():
                try:
                    order_book = connector.get_l2_order_book('BTCUSDT')
                    storage.add_snapshot(exchange, 'BTC/USD', order_book['bids'], order_book['asks'])
                except Exception as e:
                    print(f"Error collecting data from {exchange}: {str(e)}")
            time.sleep(1)  # Collect every second
    
    data_thread = threading.Thread(target=collect_data, daemon=True)
    data_thread.start()
    
    # Run performance test
    print("Running performance test...")
    results = order_manager.performance_test('binance', 'BTCUSDT')
    print(f"Performance results: {results}")
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")

if __name__ == "__main__":
    main()