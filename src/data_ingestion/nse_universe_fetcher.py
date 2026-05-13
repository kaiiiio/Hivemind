"""
HIVEMIND - Multi-Agent AI Trading System
Data Ingestion Layer - Phase 1: F&O Universe Definition

This module downloads the official F&O constituent list from NSE
and maintains the master universe of ~185 liquid stocks.
"""

import requests
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
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


class FOUniverseDownloader:
    """Downloads and manages F&O universe from NSE."""
    
    def __init__(self, data_dir: str = None):
        """
        Initialize the downloader.
        
        Args:
            data_dir: Directory to store downloaded CSV files
        """
        self.data_dir = Path(data_dir) if data_dir else Path(os.getenv('DATA_DIR', './data'))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # NSE endpoints with proper headers
        self.base_url = "https://www.nseindia.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        
    def download_fo_mktlots(self) -> Optional[pd.DataFrame]:
        """
        Download the F&O market lots CSV from NSE.
        
        Returns:
            DataFrame with ticker, company_name, lot_size or None if failed
        """
        url = f"{self.base_url}/api/market-data/fo-mktlots"
        
        try:
            logger.info(f"Downloading F&O market lots from {url}")
            
            # First hit the homepage to get cookies
            self.session.get(f"{self.base_url}/", timeout=10)
            
            # Then download the actual data
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            # Parse JSON response
            data = response.json()
            
            # Extract relevant fields
            records = []
            for item in data.get('records', []):
                records.append({
                    'ticker': item.get('symbol', ''),
                    'company_name': item.get('companyName', ''),
                    'lot_size': item.get('marketLot', 0),
                    'is_active': item.get('isActive', True)
                })
            
            df = pd.DataFrame(records)
            
            if not df.empty:
                # Save raw CSV
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                csv_path = self.data_dir / f"fo_mktlots_{timestamp}.csv"
                df.to_csv(csv_path, index=False)
                logger.info(f"Saved F&O market lots to {csv_path} ({len(df)} records)")
            
            return df
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download F&O market lots: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error downloading F&O market lots: {e}")
            return None
    
    def clean_and_validate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and validate the F&O universe data.
        
        Args:
            df: Raw DataFrame from NSE
            
        Returns:
            Cleaned DataFrame
        """
        if df is None or df.empty:
            return pd.DataFrame()
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['ticker'])
        
        # Remove rows with empty tickers
        df = df[df['ticker'].notna() & (df['ticker'] != '')]
        
        # Standardize ticker format (remove any special characters)
        df['ticker'] = df['ticker'].str.strip().str.upper()
        
        # Ensure lot_size is integer
        df['lot_size'] = pd.to_numeric(df['lot_size'], errors='coerce').fillna(0).astype(int)
        
        # Add metadata
        df['added_date'] = datetime.now()
        df['last_updated'] = datetime.now()
        
        logger.info(f"Cleaned F&O universe: {len(df)} valid tickers")
        return df


def run_phase1() -> tuple[List[str], pd.DataFrame]:
    """
    Execute Phase 1: F&O Universe Definition.
    
    Returns:
        Tuple of (List of active F&O ticker symbols, cleaned DataFrame)
    """
    logger.info("=" * 60)
    logger.info("PHASE 1: F&O Universe Definition")
    logger.info("=" * 60)
    
    downloader = FOUniverseDownloader()
    
    # Download from NSE
    df_raw = downloader.download_fo_mktlots()
    
    if df_raw is None or df_raw.empty:
        logger.error("Phase 1 failed: Could not download F&O universe")
        return [], pd.DataFrame()
    
    # Clean and validate
    df_clean = downloader.clean_and_validate(df_raw)
    
    if df_clean.empty:
        logger.error("Phase 1 failed: No valid tickers after cleaning")
        return [], pd.DataFrame()
    
    # Return tickers from cleaned DataFrame
    tickers = df_clean['ticker'].tolist()
    
    logger.info(f"Phase 1 complete: {len(tickers)} F&O tickers available")
    logger.info("=" * 60)
    
    return tickers, df_clean


if __name__ == "__main__":
    # Test run without database
    tickers, df = run_phase1()
    print(f"\nDownloaded {len(tickers)} F&O tickers:")
    print(tickers[:10], "...")  # Show first 10
