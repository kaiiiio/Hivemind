"""
HIVEMIND - Multi-Agent AI Trading System
Data Ingestion Layer - Phase 3: Market Regime Assessment

This module checks market conditions (VIX, FII/DII flows) to determine
if the market is in RISK_ON, RISK_OFF, or CAUTIOUS regime.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
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
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    logger.warning("yfinance not installed. Install with: pip install yfinance")


class MarketRegimeAnalyzer:
    """Analyzes market conditions to determine trading regime."""
    
    def __init__(self):
        """Initialize the regime analyzer."""
        self.vix_percentile_threshold = int(os.getenv('RISK_OFF_VIX_PERCENTILE', '85'))
        self.fii_flow_threshold = float(os.getenv('FII_FLOW_THRESHOLD', '-5000'))
        
    def get_vix_data(self, period: int = 60) -> Optional[pd.DataFrame]:
        """
        Download India VIX data.
        
        Args:
            period: Number of days of historical data
            
        Returns:
            DataFrame with VIX OHLC data
        """
        if not YFINANCE_AVAILABLE:
            logger.error("yfinance not available")
            return None
        
        try:
            logger.info("Downloading India VIX data...")
            vix = yf.Ticker("^INDIAVIX")
            df = vix.history(period=f"{period}d")
            
            if df.empty:
                logger.warning("No VIX data received")
                return None
            
            logger.info(f"Downloaded {len(df)} days of VIX data")
            return df
            
        except Exception as e:
            logger.error(f"Failed to download VIX data: {e}")
            return None
    
    def calculate_vix_percentile(self, current_vix: float, historical_vix: pd.Series) -> float:
        """
        Calculate the percentile rank of current VIX vs historical values.
        
        Args:
            current_vix: Current VIX close value
            historical_vix: Series of historical VIX closes
            
        Returns:
            Percentile rank (0-100)
        """
        percentile = (historical_vix < current_vix).sum() / len(historical_vix) * 100
        return round(percentile, 2)
    
    def get_fii_dii_flows(self, days: int = 15) -> Optional[Dict]:
        """
        Get FII/DII flow data from NSE.
        
        Args:
            days: Number of days to fetch
            
        Returns:
            Dictionary with FII/DII flow statistics
        """
        # Note: This is a simplified version. In production, you'd scrape NSE reports
        # For now, we'll use a placeholder that can be enhanced later
        
        try:
            logger.info("Fetching FII/DII flow data...")
            
            # Placeholder: In production, this would scrape NSE's daily reports
            # URL: https://www.nseindia.com/reports/daily-report/capital-market
            
            # For testing, return mock data structure
            flow_data = {
                'fii_flows': [],  # List of daily FII net flows (in crores)
                'dii_flows': [],  # List of daily DII net flows (in crores)
                'dates': []
            }
            
            logger.warning("FII/DII flow scraping not yet implemented - using placeholder")
            return flow_data
            
        except Exception as e:
            logger.error(f"Failed to fetch FII/DII flows: {e}")
            return None
    
    def get_nifty_data(self, period: int = 60) -> Optional[pd.DataFrame]:
        """
        Download Nifty 50 data for market context.
        
        Args:
            period: Number of days of historical data
            
        Returns:
            DataFrame with Nifty OHLC data
        """
        if not YFINANCE_AVAILABLE:
            return None
        
        try:
            logger.info("Downloading Nifty 50 data...")
            nifty = yf.Ticker("^NSEI")
            df = nifty.history(period=f"{period}d")
            
            if df.empty:
                logger.warning("No Nifty data received")
                return None
            
            logger.info(f"Downloaded {len(df)} days of Nifty data")
            return df
            
        except Exception as e:
            logger.error(f"Failed to download Nifty data: {e}")
            return None
    
    def analyze_regime(self) -> Dict:
        """
        Perform comprehensive regime analysis.
        
        Returns:
            Dictionary with regime status and supporting metrics
        """
        logger.info("=" * 60)
        logger.info("PHASE 3: Market Regime Assessment")
        logger.info("=" * 60)
        
        result = {
            'trade_date': datetime.now().date(),
            'vix_close': None,
            'vix_10d_avg': None,
            'vix_percentile': None,
            'fii_flow_10d_sum': None,
            'dii_flow_10d_sum': None,
            'nifty_change_pct': None,
            'regime_status': 'CAUTIOUS',
            'regime_reason': 'Pending analysis',
            'created_at': datetime.now()
        }
        
        # Step 1: Analyze VIX
        vix_df = self.get_vix_data(period=60)
        if vix_df is not None and not vix_df.empty:
            result['vix_close'] = round(vix_df['Close'].iloc[-1], 2)
            result['vix_10d_avg'] = round(vix_df['Close'].tail(10).mean(), 2)
            result['vix_percentile'] = self.calculate_vix_percentile(
                result['vix_close'], 
                vix_df['Close'][:-1]  # Exclude current day
            )
            logger.info(f"VIX Close: {result['vix_close']}, 10d Avg: {result['vix_10d_avg']}, Percentile: {result['vix_percentile']}")
        
        # Step 2: Get FII/DII flows
        flow_data = self.get_fii_dii_flows(days=15)
        if flow_data and flow_data.get('fii_flows'):
            fii_flows = flow_data['fii_flows']
            dii_flows = flow_data['dii_flows']
            result['fii_flow_10d_sum'] = sum(fii_flows[:10]) if len(fii_flows) >= 10 else sum(fii_flows)
            result['dii_flow_10d_sum'] = sum(dii_flows[:10]) if len(dii_flows) >= 10 else sum(dii_flows)
            logger.info(f"FII 10d Sum: {result['fii_flow_10d_sum']}, DII 10d Sum: {result['dii_flow_10d_sum']}")
        
        # Step 3: Get Nifty change
        nifty_df = self.get_nifty_data(period=60)
        if nifty_df is not None and not nifty_df.empty:
            latest_close = nifty_df['Close'].iloc[-1]
            prev_close = nifty_df['Close'].iloc[-2] if len(nifty_df) > 1 else latest_close
            result['nifty_change_pct'] = round((latest_close - prev_close) / prev_close * 100, 2)
            logger.info(f"Nifty Change: {result['nifty_change_pct']}%")
        
        # Step 4: Determine regime
        regime, reason = self._determine_regime(result)
        result['regime_status'] = regime
        result['regime_reason'] = reason
        
        logger.info(f"REGIME DECISION: {regime} - {reason}")
        logger.info("=" * 60)
        
        return result
    
    def _determine_regime(self, metrics: Dict) -> Tuple[str, str]:
        """
        Determine market regime based on metrics.
        
        Args:
            metrics: Dictionary of market metrics
            
        Returns:
            Tuple of (regime_status, reason)
        """
        vix_percentile = metrics.get('vix_percentile', 50)
        fii_flow_10d = metrics.get('fii_flow_10d_sum', 0)
        nifty_change = metrics.get('nifty_change_pct', 0)
        
        reasons = []
        
        # Check for RISK_OFF conditions
        risk_off_signals = 0
        
        if vix_percentile >= self.vix_percentile_threshold:
            risk_off_signals += 1
            reasons.append(f"VIX at {vix_percentile}th percentile (threshold: {self.vix_percentile_threshold})")
        
        if fii_flow_10d is not None and fii_flow_10d < self.fii_flow_threshold:
            risk_off_signals += 1
            reasons.append(f"FII outflow {fii_flow_10d} below threshold {self.fii_flow_threshold}")
        
        if nifty_change is not None and nifty_change < -2:
            risk_off_signals += 1
            reasons.append(f"Nifty down {nifty_change}% (sharp decline)")
        
        # Determine regime
        if risk_off_signals >= 2:
            return 'RISK_OFF', '; '.join(reasons)
        elif risk_off_signals == 1:
            return 'CAUTIOUS', '; '.join(reasons) if reasons else 'Mixed signals'
        else:
            return 'RISK_ON', 'All indicators favorable for long positions'


def run_phase3() -> Dict:
    """
    Execute Phase 3: Market Regime Assessment.
    
    Returns:
        Dictionary with regime assessment
    """
    analyzer = MarketRegimeAnalyzer()
    
    # Perform analysis
    regime_data = analyzer.analyze_regime()
    
    return regime_data


if __name__ == "__main__":
    # Test run
    regime = run_phase3()
    print(f"\nMarket Regime: {regime['regime_status']}")
    print(f"Reason: {regime['regime_reason']}")
    print(f"\nKey Metrics:")
    print(f"  VIX Close: {regime.get('vix_close')}")
    print(f"  VIX Percentile: {regime.get('vix_percentile')}%")
    print(f"  Nifty Change: {regime.get('nifty_change_pct')}%")
