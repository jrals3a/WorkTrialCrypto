# data/historical_storage.py
# import time, pandas, pyarrow, pyarrow.parquet
import time
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime
from typing import Dict, List

# define class HistoricalDataStorage
# define __init__
class HistoricalDataStorage:
    def __init__(self, storage_type: str = 'local', config: Dict = None):
        self.storage_type = storage_type
        self.config = config or {}
        self.buffer = []
        self.last_flush = time.time()
        
        if storage_type == 's3':
            import boto3
            self.s3_client = boto3.client('s3')
            self.bucket_name = config.get('bucket_name', 'crypto-data-lake')
    
    # define add_snapshot
    def add_snapshot(self, exchange: str, pair: str, bids: List, asks: List):
        """Add order book snapshot to buffer"""
        timestamp = datetime.utcnow()
        self.buffer.append({
            'timestamp': timestamp,
            'exchange': exchange,
            'pair': pair,
            'bids': bids,
            'asks': asks
        })
        
        # Flush if buffer size exceeds threshold or time elapsed
        if len(self.buffer) >= self.config.get('buffer_size', 100) or \
           time.time() - self.last_flush >= self.config.get('flush_interval', 60):
            self.flush()
    
    # define flush
    def flush(self):
        """Write buffer to storage"""
        if not self.buffer:
            return
        
        df = pd.DataFrame(self.buffer)
        table = pa.Table.from_pandas(df)
        
        if self.storage_type == 'local':
            # Write to local parquet file
            date_str = datetime.utcnow().strftime('%Y-%m-%d')
            filename = f"orderbook_data/{date_str}/snapshots_{int(time.time())}.parquet"
            pq.write_table(table, filename)
        
        elif self.storage_type == 's3':
            # Write to S3
            date_str = datetime.utcnow().strftime('%Y-%m-%d')
            filename = f"orderbook_data/{date_str}/snapshots_{int(time.time())}.parquet"
            
            with pa.BufferOutputStream() as buf:
                pq.write_table(table, buf)
                self.s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=filename,
                    Body=buf.getvalue().to_pybytes()
                )
        
        self.buffer = []
        self.last_flush = time.time()