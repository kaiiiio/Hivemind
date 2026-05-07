"""
HIVEMIND - Multi-Agent AI Trading System
Data Ingestion Layer - Phase 4 & 5: Bhavcopy & OHLCV Data

This module downloads NSE Bhavcopy files and targeted OHLCV data
for the survivor stocks.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Set, Dict, Optional
import logging
from dotenv import load_dotenv
import os
import zipfile
import io

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    logger.warning("yfinance not installed")

try:
    from jugaad_data import nse
    JUGAAD_AVAILABLE = True
except ImportError:
    JUGAAD_AVAILABLE = False
    logger.warning("jugaad_data not installed. Install with: pip install jugaad_data")


class BhavcopyDownloader:
    """Downloads and processes NSE Bhavcopy data."""
    
    def __init__(self, data_dir: str = None):
        """
        Initialize the downloader.
        
        Args:
            data_dir: Directory to store downloaded files
        """
        self.data_dir = Path(data_dir) if data_dir else Path(os.getenv('DATA_DIR', './data'))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def download_equity_bhavcopy(self, trade_date: datetime = None) -> Optional[pd.DataFrame]:
        """
        Download equity bhavcopy for a specific date using jugaad_data.
        
        Args:
            trade_date: Date for which to download bhavcopy (default: today)
            
        Returns:
            DataFrame with bhavcopy data
        """
        if not JUGAAD_AVAILABLE:
            logger.error("jugaad_data not available")
            return None
        
        if trade_date is None:
            trade_date = datetime.now()
        
        try:
            logger.info(f"Downloading equity bhavcopy for {trade_date.date()}...")
            
            # Use jugaad_data's NSE client
            nse_client = nse.NSE()
            
            # Download bhavcopy
            bhavcopy_df = nse_client.bhavcopy(trade_date.date())
            
            if bhavcopy_df is None or bhavcopy_df.empty:
                logger.warning("No bhavcopy data received")
                return None
            
            logger.info(f"Downloaded {len(bhavcopy_df)} records from equity bhavcopy")
            
            # Save raw file
            timestamp = trade_date.strftime('%Y%m%d')
            csv_path = self.data_dir / f"equity_bhavcopy_{timestamp}.csv"
            bhavcopy_df.to_csv(csv_path, index=False)
            logger.info(f"Saved raw bhavcopy to {csv_path}")
            
            return bhavcopy_df
            
        except Exception as e:
            logger.error(f"Failed to download equity bhavcopy: {e}")
            return None
    
    def download_fo_bhavcopy(self, trade_date: datetime = None) -> Optional[pd.DataFrame]:
        """
        Download F&O bhavcopy for a specific date.
        
        Args:
            trade_date: Date for which to download bhavcopy
            
        Returns:
            DataFrame with F&O bhavcopy data
        """
        if not JUGAAD_AVAILABLE:
            return None
        
        if trade_date is None:
            trade_date = datetime.now()
        
        try:
            logger.info(f"Downloading F&O bhavcopy for {trade_date.date()}...")
            
            nse_client = nse.NSE()
            
            # Download F&O bhavcopy
            fo_bhavcopy_df = nse_client.fobhavcopy(trade_date.date())
            
            if fo_bhavcopy_df is None or fo_bhavcopy_df.empty:
                logger.warning("No F&O bhavcopy data received")
                return None
            
            logger.info(f"Downloaded {len(fo_bhavcopy_df)} records from F&O bhavcopy")
            
            # Save raw file
            timestamp = trade_date.strftime('%Y%m%d')
            csv_path = self.data_dir / f"fo_bhavcopy_{timestamp}.csv"
            fo_bhavcopy_df.to_csv(csv_path, index=False)
            logger.info(f"Saved raw F&O bhavcopy to {csv_path}")
            
            return fo_bhavcopy_df
            
        except Exception as e:
            logger.error(f"Failed to download F&O bhavcopy: {e}")
            return None
    
    def extract_delivery_data(self, equity_df: pd.DataFrame, tickers: Set[str]) -> pd.DataFrame:
        """
        Extract delivery quantity and calculate delivery ratio from equity bhavcopy.
        
        Args:
            equity_df: Raw equity bhavcopy DataFrame
            tickers: Set of survivor tickers to filter
            
        Returns:
            DataFrame with delivery metrics
        """
        if equity_df is None or equity_df.empty:
            return pd.DataFrame()
        
        # Filter to our survivor tickers
        equity_df = equity_df[equity_df['SYMBOL'].isin(tickers)].copy()
        
        if equity_df.empty:
            logger.warning("No matching tickers in equity bhavcopy")
            return pd.DataFrame()
        
        # Extract relevant columns
        delivery_df = pd.DataFrame({
            'ticker': equity_df['SYMBOL'],
            'time': datetime.now(),
            'deliverable_quantity': equity_df['DELIV_QTY'],
            'total_quantity': equity_df['TOT_TRD_QTY'],
        })
        
        # Calculate delivery ratio
        delivery_df['delivery_ratio'] = (
            delivery_df['deliverable_quantity'] / 
            delivery_df['total_quantity'].replace(0, np.nan)
        ).round(4)
        
        logger.info(f"Extracted delivery data for {len(delivery_df)} tickers")
        return delivery_df
    
    def extract_oi_data(self, fo_df: pd.DataFrame, tickers: Set[str]) -> pd.DataFrame:
        """
        Extract Open Interest data from F&O bhavcopy.
        
        Args:
            fo_df: Raw F&O bhavcopy DataFrame
            tickers: Set of survivor tickers to filter
            
        Returns:
            DataFrame with OI metrics
        """
        if fo_df is None or fo_df.empty:
            return pd.DataFrame()
        
        # Filter to our survivor tickers (FUT symbols)
        fo_df = fo_df[fo_df['SYMBOL'].isin(tickers)].copy()
        
        if fo_df.empty:
            logger.warning("No matching tickers in F&O bhavcopy")
            return pd.DataFrame()
        
        # Extract relevant columns for futures
        oi_df = pd.DataFrame({
            'ticker': fo_df['SYMBOL'],
            'time': datetime.now(),
            'oi_open_interest': fo_df['OPEN_INT'],
            'oi_change': fo_df['CHG_IN_OI'],
        })
        
        logger.info(f"Extracted OI data for {len(oi_df)} tickers")
        return oi_df


class OHLCVDownloader:
    """Downloads historical OHLCV data using yfinance."""
    
    def __init__(self, data_dir: str = None):
        """
        Initialize the downloader.
        
        Args:
            data_dir: Directory to store downloaded files
        """
        self.data_dir = Path(data_dir) if data_dir else Path(os.getenv('DATA_DIR', './data'))
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def download_ohlcv(self, tickers: List[str], period: int = 250) -> Optional[Dict[str, pd.DataFrame]]:
        """
        Download OHLCV data for multiple tickers.
        
        Args:
            tickers: List of ticker symbols
            period: Number of days of historical data
            
        Returns:
            Dictionary mapping ticker to OHLCV DataFrame
        """
        if not YFINANCE_AVAILABLE:
            logger.error("yfinance not available")
            return None
        
        if not tickers:
            logger.warning("No tickers provided")
            return None
        
        try:
            logger.info(f"Downloading OHLCV data for {len(tickers)} tickers...")
            
            # Convert tickers to yfinance format (add .NS for NSE)
            yf_tickers = [f"{t}.NS" for t in tickers]
            
            # Download all at once (more efficient than individual calls)
            data = yf.download(yf_tickers, period=f"{period}d", progress=False)
            
            if data is None or data.empty:
                logger.warning("No OHLCV data received")
                return None
            
            logger.info(f"Downloaded OHLCV data for {len(tickers)} tickers")
            
            # Handle multi-level columns if present
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.droplevel(1)
            
            # Save combined data
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            csv_path = self.data_dir / f"ohlcv_combined_{timestamp}.csv"
            data.to_csv(csv_path)
            logger.info(f"Saved combined OHLCV data to {csv_path}")
            
            return data
            
        except Exception as e:
            logger.error(f"Failed to download OHLCV data: {e}")
            return None
    
    def download_individual_ticker(self, ticker: str, period: int = 250) -> Optional[pd.DataFrame]:
        """
        Download OHLCV for a single ticker (fallback method).
        
        Args:
            ticker: Ticker symbol
            period: Number of days
            
        Returns:
            DataFrame with OHLCV data
        """
        if not YFINANCE_AVAILABLE:
            return None
        
        try:
            yf_ticker = f"{ticker}.NS"
            df = yf.Ticker(yf_ticker).history(period=f"{period}d")
            
            if df is None or df.empty:
                return None
            
            logger.info(f"Downloaded {len(df)} days for {ticker}")
            return df
            
        except Exception as e:
            logger.error(f"Failed to download {ticker}: {e}")
            return None


def run_phase4_5(survivor_tickers: Set[str], db_connection=None) -> Dict:
    """
    Execute Phase 4 (Bhavcopy/Microstructure) and Phase 5 (OHLCV Hydration).
    
    Args:
        survivor_tickers: Set of survivor stock tickers
        db_connection: Optional database connection
        
    Returns:
        Dictionary with downloaded data
    """
    logger.info("=" * 60)
    logger.info("PHASE 4 & 5: Bhavcopy & OHLCV Data Extraction")
    logger.info("=" * 60)
    
    results = {
        'delivery_data': None,
        'oi_data': None,
        'ohlcv_data': None,
        'tickers_processed': len(survivor_tickers)
    }
    
    # Phase 4: Download Bhavcopy
    bhavcopy_downloader = BhavcopyDownloader()
    
    equity_df = bhavcopy_downloader.download_equity_bhavcopy()
    fo_df = bhavcopy_downloader.download_fo_bhavcopy()
    
    if equity_df is not None:
        delivery_data = bhavcopy_downloader.extract_delivery_data(equity_df, survivor_tickers)
        results['delivery_data'] = delivery_data
        
        if not delivery_data.empty:
            logger.info(f"Delivery data: {len(delivery_data)} tickers")
    
    if fo_df is not None:
        oi_data = bhavcopy_downloader.extract_oi_data(fo_df, survivor_tickers)
        results['oi_data'] = oi_data
        
        if not oi_data.empty:
            logger.info(f"OI data: {len(oi_data)} tickers")
    
    # Phase 5: Download OHLCV
    ohlcv_downloader = OHLCVDownloader()
    
    ohlcv_data = ohlcv_downloader.download_ohlcv(list(survivor_tickers), period=250)
    results['ohlcv_data'] = ohlcv_data
    
    if ohlcv_data is not None:
        logger.info(f"OHLCV data shape: {ohlcv_data.shape}")
    
    logger.info("=" * 60)
    logger.info(f"Phases 4-5 complete: Processed {len(survivor_tickers)} tickers")
    logger.info("=" * 60)
    
    return results


if __name__ == "__main__":
    # Test run with sample tickers
    sample_tickers = {'RELIANCE', 'TCS', 'INFY', 'HDFCBANK', 'ICICIBANK'}
    
    results = run_phase4_5(sample_tickers)
    
    print(f"\nResults:")
    print(f"  Tickers processed: {results['tickers_processed']}")
    print(f"  Delivery data: {type(results['delivery_data'])}")
    print(f"  OI data: {type(results['oi_data'])}")
    print(f"  OHLCV data: {type(results['ohlcv_data'])}")
