"""
HIVEMIND - Multi-Agent AI Trading System
Data Ingestion Layer - Phase 6: Database Upsert

This module consolidates all downloaded data and upserts into TimescaleDB.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    import psycopg2
    from psycopg2.extras import execute_batch
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    logger.warning("psycopg2 not installed. Install with: pip install psycopg2-binary")


class DatabaseManager:
    """Manages database connections and upsert operations."""
    
    def __init__(self):
        """Initialize database connection from environment variables."""
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', '5432')),
            'database': os.getenv('DB_NAME', 'hivemind'),
            'user': os.getenv('DB_USER', 'hivemind'),
            'password': os.getenv('DB_PASSWORD', 'hivemind_password')
        }
        
        self.connection = None
    
    def connect(self) -> bool:
        """
        Establish database connection.
        
        Returns:
            True if successful, False otherwise
        """
        if not PSYCOPG2_AVAILABLE:
            logger.error("psycopg2 not available")
            return False
        
        try:
            self.connection = psycopg2.connect(**self.db_config)
            logger.info(f"Connected to database: {self.db_config['database']}@{self.db_config['host']}")
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
    
    def upsert_daily_prices(self, ohlcv_data: Dict[str, pd.DataFrame], tickers: List[str]) -> int:
        """
        Upsert OHLCV data into daily_prices hypertable.
        
        Args:
            ohlcv_data: Dictionary mapping ticker to OHLCV DataFrame
            tickers: List of ticker symbols
            
        Returns:
            Number of records inserted
        """
        if not self.connection or ohlcv_data is None:
            return 0
        
        count = 0
        
        try:
            with self.connection.cursor() as cursor:
                for ticker in tickers:
                    if ticker not in ohlcv_data:
                        continue
                    
                    df = ohlcv_data[ticker]
                    
                    # Handle different column naming conventions
                    if isinstance(df.columns, pd.MultiIndex):
                        df = df.copy()
                        df.columns = df.columns.droplevel(1)
                    
                    # Prepare data for insertion
                    records = []
                    for idx, row in df.iterrows():
                        records.append({
                            'time': idx.to_pydatetime() if hasattr(idx, 'to_pydatetime') else idx,
                            'ticker': ticker,
                            'open': row.get('Open', row.get('open')),
                            'high': row.get('High', row.get('high')),
                            'low': row.get('Low', row.get('low')),
                            'close': row.get('Close', row.get('close')),
                            'volume': int(row.get('Volume', row.get('volume', 0))),
                            'adj_close': row.get('Adj Close', row.get('adj_close'))
                        })
                    
                    if not records:
                        continue
                    
                    # Batch insert for efficiency
                    query = """
                        INSERT INTO daily_prices (time, ticker, open, high, low, close, volume, adj_close)
                        VALUES (%(time)s, %(ticker)s, %(open)s, %(high)s, %(low)s, %(close)s, %(volume)s, %(adj_close)s)
                        ON CONFLICT (time, ticker) DO UPDATE SET
                            open = EXCLUDED.open,
                            high = EXCLUDED.high,
                            low = EXCLUDED.low,
                            close = EXCLUDED.close,
                            volume = EXCLUDED.volume,
                            adj_close = EXCLUDED.adj_close
                    """
                    
                    execute_batch(cursor, query, records, page_size=100)
                    count += len(records)
            
            self.connection.commit()
            logger.info(f"Upserted {count} daily price records")
            return count
            
        except Exception as e:
            logger.error(f"Failed to upsert daily prices: {e}")
            self.connection.rollback()
            return 0
    
    def upsert_delivery_data(self, delivery_df: pd.DataFrame, oi_df: pd.DataFrame) -> int:
        """
        Upsert delivery and OI data into delivery_data hypertable.
        
        Args:
            delivery_df: DataFrame with delivery metrics
            oi_df: DataFrame with OI metrics
            
        Returns:
            Number of records inserted
        """
        if not self.connection:
            return 0
        
        count = 0
        
        try:
            with self.connection.cursor() as cursor:
                # Merge delivery and OI data
                if delivery_df is not None and not delivery_df.empty:
                    for _, row in delivery_df.iterrows():
                        cursor.execute("""
                            INSERT INTO delivery_data 
                                (time, ticker, deliverable_quantity, total_quantity, delivery_ratio)
                            VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT (time, ticker) DO UPDATE SET
                                deliverable_quantity = EXCLUDED.deliverable_quantity,
                                total_quantity = EXCLUDED.total_quantity,
                                delivery_ratio = EXCLUDED.delivery_ratio
                        """, (
                            row['time'],
                            row['ticker'],
                            row['deliverable_quantity'],
                            row['total_quantity'],
                            row['delivery_ratio']
                        ))
                        count += 1
                
                if oi_df is not None and not oi_df.empty:
                    for _, row in oi_df.iterrows():
                        cursor.execute("""
                            INSERT INTO delivery_data 
                                (time, ticker, oi_open_interest, oi_change)
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT (time, ticker) DO UPDATE SET
                                oi_open_interest = EXCLUDED.oi_open_interest,
                                oi_change = EXCLUDED.oi_change
                        """, (
                            row['time'],
                            row['ticker'],
                            row['oi_open_interest'],
                            row['oi_change']
                        ))
                        count += 1
            
            self.connection.commit()
            logger.info(f"Upserted {count} delivery/OI records")
            return count
            
        except Exception as e:
            logger.error(f"Failed to upsert delivery data: {e}")
            self.connection.rollback()
            return 0
    
    def get_survivor_tickers(self) -> Set[str]:
        """
        Get survivor tickers from database.
        
        Returns:
            Set of ticker symbols
        """
        if not self.connection:
            return set()
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT ticker FROM screener_survivors
                    WHERE is_survivor = TRUE
                """)
                results = cursor.fetchall()
                tickers = {row[0] for row in results}
                logger.info(f"Retrieved {len(tickers)} survivor tickers from database")
                return tickers
        except Exception as e:
            logger.error(f"Failed to retrieve survivor tickers: {e}")
            return set()


def run_phase6(data_results: Dict, db_manager: DatabaseManager) -> bool:
    """
    Execute Phase 6: Database Upsert.
    
    Args:
        data_results: Dictionary with data from phases 4-5
        db_manager: DatabaseManager instance
        
    Returns:
        True if successful, False otherwise
    """
    logger.info("=" * 60)
    logger.info("PHASE 6: Database Upsert")
    logger.info("=" * 60)
    
    if not db_manager.connection:
        logger.error("No database connection")
        return False
    
    success = True
    
    # Upsert OHLCV data
    ohlcv_data = data_results.get('ohlcv_data')
    if ohlcv_data is not None:
        tickers = list(data_results.get('tickers_processed', []))
        count = db_manager.upsert_daily_prices(ohlcv_data, tickers)
        if count == 0:
            success = False
    
    # Upsert delivery and OI data
    delivery_df = data_results.get('delivery_data')
    oi_df = data_results.get('oi_data')
    
    if delivery_df is not None or oi_df is not None:
        count = db_manager.upsert_delivery_data(delivery_df, oi_df)
        if count == 0 and (delivery_df is not None or oi_df is not None):
            logger.warning("No delivery/OI records upserted")
    
    logger.info("=" * 60)
    logger.info(f"Phase 6 complete: {'SUCCESS' if success else 'PARTIAL'}")
    logger.info("=" * 60)
    
    return success


if __name__ == "__main__":
    # Test database connection
    db_mgr = DatabaseManager()
    
    if db_mgr.connect():
        print("Database connection successful!")
        db_mgr.disconnect()
    else:
        print("Database connection failed. Check your .env configuration.")
