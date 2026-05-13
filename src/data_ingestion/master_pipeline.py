"""
HIVEMIND - Multi-Agent AI Trading System
Master Data Ingestion Pipeline

This is the main entry point that orchestrates all 6 phases of data ingestion.
Run this daily at 18:30 IST via cron.
"""

import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Set, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# Configure logging
log_dir = Path(__file__).parent.parent.parent / 'logs'
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / f"ingestion_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def run_full_pipeline():
    """
    Execute the complete data ingestion pipeline (all 6 phases).
    
    Returns:
        Dictionary with pipeline results
    """
    logger.info("=" * 80)
    logger.info("HIVEMIND DATA INGESTION PIPELINE")
    logger.info(f"Started at: {datetime.now().isoformat()}")
    logger.info("=" * 80)
    
    results = {
        'success': False,
        'phases_completed': [],
        'survivor_tickers': [],
        'regime_status': None,
        'errors': []
    }
    
    db_manager = None
    
    try:
        # Import database manager
        from data_ingestion.database_upsert import DatabaseManager
        
        # Initialize database connection
        db_manager = DatabaseManager()
        
        if not db_manager.connect():
            logger.error("Failed to connect to database. Continuing without DB operations.")
            db_manager = None
        
        # ========================================
        # PHASE 1: F&O Universe Definition
        # ========================================
        try:
            from data_ingestion.nse_universe_fetcher import run_phase1
            
            fo_tickers, df_clean = run_phase1()
            
            if not fo_tickers:
                raise Exception("Phase 1 failed: No F&O tickers downloaded")
            
            if db_manager:
                db_manager.upsert_fo_universe(df_clean)
            
            results['phases_completed'].append('nse_universe_fetcher')
            logger.info(f"✓ Phase 1 complete: {len(fo_tickers)} F&O tickers")
            
        except Exception as e:
            logger.error(f"Phase 1 failed: {e}")
            results['errors'].append(f"Phase 1: {str(e)}")
            return results
        
        # ========================================
        # PHASE 2: Screener.in Fundamental Filtering
        # ========================================
        try:
            from data_ingestion.screener_fundamentals import run_phase2
            import asyncio
            
            fo_ticker_set = set(fo_tickers)
            survivor_tickers, df_filtered = asyncio.run(run_phase2(
                fo_tickers=fo_ticker_set
            ))
            
            if not survivor_tickers:
                logger.warning("Phase 2 returned no survivors. Using F&O universe as fallback.")
                survivor_tickers = fo_tickers
            else:
                if db_manager:
                    db_manager.upsert_screener_survivors(df_filtered)
                results['phases_completed'].append('screener_fundamentals')
                logger.info(f"✓ Phase 2 complete: {len(survivor_tickers)} survivor stocks")
            
            survivor_ticker_set = set(survivor_tickers)
            results['survivor_tickers'] = survivor_tickers
            
        except Exception as e:
            logger.error(f"Phase 2 failed: {e}")
            results['errors'].append(f"Phase 2: {str(e)}")
            survivor_ticker_set = set(fo_tickers)
            results['survivor_tickers'] = fo_tickers
        
        # ========================================
        # PHASE 3: Market Regime Assessment
        # ========================================
        try:
            from data_ingestion.market_regime_checker import run_phase3
            
            regime_data = run_phase3()
            
            if db_manager:
                db_manager.upsert_market_regime(regime_data)
            
            results['regime_status'] = regime_data.get('regime_status')
            results['phases_completed'].append('market_regime_checker')
            logger.info(f"✓ Phase 3 complete: Market regime = {regime_data['regime_status']}")
            
            # If RISK_OFF, we can halt further processing
            if regime_data['regime_status'] == 'RISK_OFF':
                logger.warning("Market is RISK_OFF. Halting long-entry processing.")
                results['phases_completed'].append('halted_risk_off')
                results['success'] = True  # Pipeline succeeded, but halted intentionally
                return results
            
        except Exception as e:
            logger.error(f"Phase 3 failed: {e}")
            results['errors'].append(f"Phase 3: {str(e)}")
            # Continue anyway - we'll default to CAUTIOUS
        
        # ========================================
        # PHASE 4 & 5: Bhavcopy & OHLCV Data
        # ========================================
        try:
            from data_ingestion.price_microstructure_loader import run_phase4_5
            
            data_results = run_phase4_5(
                survivor_tickers=survivor_ticker_set,
                db_connection=None  # DB handling is in phase 6
            )
            
            results['phases_completed'].append('price_microstructure_loader')
            logger.info(f"✓ Phases 4-5 complete: Data extracted for {len(survivor_ticker_set)} tickers")
            
        except Exception as e:
            logger.error(f"Phases 4-5 failed: {e}")
            results['errors'].append(f"Phases 4-5: {str(e)}")
            data_results = {}
        
        # ========================================
        # PHASE 6: Database Upsert
        # ========================================
        if db_manager and data_results:
            try:
                from data_ingestion.database_upsert import run_phase6
                
                success = run_phase6(data_results, db_manager)
                
                if success:
                    results['phases_completed'].append('database_upsert')
                    logger.info(f"✓ Phase 6 complete: All data upserted to database")
                else:
                    logger.warning("Phase 6 completed with partial success")
                    results['errors'].append("Phase 6: Partial upsert failure")
                    
            except Exception as e:
                logger.error(f"Phase 6 failed: {e}")
                results['errors'].append(f"Phase 6: {str(e)}")
        
        # ========================================
        # PIPELINE COMPLETE
        # ========================================
        results['success'] = len(results['errors']) == 0
        
        logger.info("=" * 80)
        logger.info("PIPELINE SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Status: {'SUCCESS' if results['success'] else 'PARTIAL'}")
        logger.info(f"Phases completed: {len(results['phases_completed'])}/6")
        logger.info(f"Survivor tickers: {len(results['survivor_tickers'])}")
        logger.info(f"Regime status: {results['regime_status']}")
        
        if results['errors']:
            logger.warning(f"Errors encountered: {len(results['errors'])}")
            for error in results['errors']:
                logger.warning(f"  - {error}")
        
        logger.info("=" * 80)
        
        return results
        
    except Exception as e:
        logger.critical(f"Pipeline crashed: {e}")
        results['errors'].append(f"Critical: {str(e)}")
        return results
    
    finally:
        # Cleanup
        if db_manager:
            db_manager.disconnect()
        
        logger.info(f"Pipeline finished at: {datetime.now().isoformat()}")


if __name__ == "__main__":
    results = run_full_pipeline()
    
    # Exit with appropriate code
    sys.exit(0 if results['success'] else 1)
