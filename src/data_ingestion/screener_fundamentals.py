"""
HIVEMIND - Multi-Agent AI Trading System
Data Ingestion Layer - Phase 2: Screener.in Fundamental Filtering

This module uses Playwright to automate login to Screener.in and download
the custom screen CSV with fundamental filters applied.
"""

import asyncio
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional, Set
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
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logger.warning("Playwright not installed. Install with: pip install playwright")


class ScreenerInDownloader:
    """Automates Screener.in login and CSV export using Playwright."""
    
    def __init__(self, data_dir: str = None):
        """
        Initialize the downloader.
        
        Args:
            data_dir: Directory to store downloaded CSV files
        """
        self.data_dir = Path(data_dir) if data_dir else Path(os.getenv('DATA_DIR', './data'))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.username = os.getenv('SCREENER_USERNAME')
        self.password = os.getenv('SCREENER_PASSWORD')
        self.screen_url = os.getenv('SCREENER_SCREEN_URL')
        
        if not all([self.username, self.password]):
            logger.warning("Screener.in credentials not found in environment variables")
        
    async def download_screen_csv(self) -> Optional[pd.DataFrame]:
        """
        Login to Screener.in and download the custom screen CSV.
        
        Returns:
            DataFrame with fundamental data or None if failed
        """
        if not PLAYWRIGHT_AVAILABLE:
            logger.error("Playwright is not available. Cannot proceed with download.")
            return None
        
        if not all([self.username, self.password, self.screen_url]):
            logger.error("Missing Screener.in credentials or screen URL")
            return None
        
        try:
            async with async_playwright() as p:
                # Launch browser in headless mode
                browser = await p.chromium.launch(
                    headless=True,
                    args=[
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-accelerated-2d-canvas',
                        '--disable-gpu'
                    ]
                )
                
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    viewport={'width': 1920, 'height': 1080}
                )
                
                page = await context.new_page()
                
                # Step 1: Navigate to login page
                logger.info("Navigating to Screener.in login page...")
                await page.goto('https://www.screener.in/login/', wait_until='networkidle')
                await asyncio.sleep(2)  # Wait for page to fully load
                
                # Step 2: Fill login form
                logger.info("Entering credentials...")
                await page.fill('input[name="username"]', self.username)
                await page.fill('input[name="password"]', self.password)
                
                # Step 3: Submit login
                await page.click('button[type="submit"]')
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(2)
                
                # Check if login was successful
                if 'login' in page.url:
                    logger.error("Login failed. Check credentials.")
                    await browser.close()
                    return None
                
                logger.info("Login successful!")
                
                # Step 4: Navigate to custom screen
                logger.info(f"Navigating to custom screen: {self.screen_url}")
                await page.goto(self.screen_url, wait_until='networkidle')
                await asyncio.sleep(2)
                
                # Step 5: Click Export to CSV
                logger.info("Clicking Export to CSV button...")
                
                # Wait for and click the export button
                export_button = page.locator('a:has-text("Export"), button:has-text("Export"), .export-btn')
                if await export_button.count() > 0:
                    # Handle download
                    async with page.expect_download() as download_info:
                        await export_button.first.click()
                        download = await download_info.value
                        
                        # Save the file
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        download_path = self.data_dir / f"screener_export_{timestamp}.csv"
                        await download.save_as(str(download_path))
                        logger.info(f"Downloaded CSV to {download_path}")
                        
                        # Read the CSV
                        df = pd.read_csv(download_path)
                        logger.info(f"Loaded {len(df)} records from Screener.in export")
                        
                        await browser.close()
                        return df
                else:
                    logger.error("Export button not found on page")
                    # Try alternative: navigate to export URL directly
                    export_url = self.screen_url.rstrip('/') + '/export/'
                    logger.info(f"Trying direct export URL: {export_url}")
                    await page.goto(export_url, wait_until='networkidle')
                    
                    # Check if download started
                    await asyncio.sleep(3)
                    
                    # For now, just parse the current page if it's CSV
                    page_content = await page.content()
                    if 'Company Name' in page_content or 'ticker' in page_content.lower():
                        # It might be a CSV displayed in browser
                        csv_path = self.data_dir / f"screener_export_{timestamp}.csv"
                        with open(csv_path, 'w') as f:
                            f.write(page_content)
                        df = pd.read_csv(csv_path)
                        logger.info(f"Loaded {len(df)} records from page content")
                        await browser.close()
                        return df
                    
                    await browser.close()
                    return None
                    
        except Exception as e:
            logger.error(f"Error during Screener.in automation: {e}")
            return None
    
    def clean_screener_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and standardize Screener.in data.
        
        Args:
            df: Raw DataFrame from Screener.in
            
        Returns:
            Cleaned DataFrame with standardized column names
        """
        if df is None or df.empty:
            return pd.DataFrame()
        
        # Standardize column names (lowercase, replace spaces with underscores)
        df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
        
        # Map common column variations to standard names
        column_mapping = {
            'name': 'company_name',
            'symbol': 'ticker',
            'market_cap': 'market_cap',
            'pe': 'pe_ratio',
            'pb': 'pb_ratio',
            'debt_to_equity': 'debt_to_equity',
            'debt/equity': 'debt_to_equity',
            'roce': 'roce',
            'promoter_holding': 'promoter_holding',
            'eps_growth_3years': 'eps_growth_3y',
            'sales_growth_3years': 'sales_growth_3y',
        }
        
        df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
        
        # Ensure ticker exists (create from company name if needed)
        if 'ticker' not in df.columns and 'company_name' in df.columns:
            df['ticker'] = df['company_name'].str.strip().str.upper().str.replace(' ', '_')
        
        # Clean numeric columns
        numeric_cols = ['market_cap', 'pe_ratio', 'pb_ratio', 'debt_to_equity', 
                       'roce', 'promoter_holding', 'eps_growth_3y', 'sales_growth_3y']
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Add metadata
        df['screen_date'] = datetime.now().date()
        df['is_survivor'] = True
        df['created_at'] = datetime.now()
        df['updated_at'] = datetime.now()
        
        logger.info(f"Cleaned Screener.in data: {len(df)} survivors")
        return df
    
    def intersect_with_fo_universe(self, screener_df: pd.DataFrame, fo_tickers: Set[str]) -> pd.DataFrame:
        """
        Filter Screener.in results to only include F&O universe stocks.
        
        Args:
            screener_df: Cleaned Screener.in DataFrame
            fo_tickers: Set of F&O ticker symbols
            
        Returns:
            Filtered DataFrame with only F&O stocks that passed screening
        """
        if screener_df is None or screener_df.empty:
            return pd.DataFrame()
        
        if not fo_tickers:
            logger.warning("No F&O tickers provided for intersection")
            return screener_df
        
        # Normalize tickers for comparison
        screener_df['ticker_normalized'] = screener_df['ticker'].str.strip().str.upper()
        fo_tickers_normalized = {t.strip().upper() for t in fo_tickers}
        
        # Filter to intersection
        filtered = screener_df[screener_df['ticker_normalized'].isin(fo_tickers_normalized)].copy()
        
        # Drop the normalized column
        filtered = filtered.drop(columns=['ticker_normalized'])
        
        logger.info(f"Intersection: {len(filtered)} stocks pass both F&O and fundamental screens")
        return filtered
    
    def save_to_database(self, df: pd.DataFrame, db_connection) -> int:
        """
        Upsert Screener.in survivors into TimescaleDB.
        
        Args:
            df: Cleaned DataFrame
            db_connection: Database connection
            
        Returns:
            Number of records inserted/updated
        """
        if df is None or df.empty:
            return 0
        
        try:
            count = 0
            with db_connection.cursor() as cursor:
                for _, row in df.iterrows():
                    cursor.execute("""
                        INSERT INTO screener_survivors (
                            ticker, company_name, market_cap, pe_ratio, pb_ratio,
                            debt_to_equity, roce, promoter_holding, eps_growth_3y,
                            sales_growth_3y, is_survivor, screen_date, created_at, updated_at
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (ticker)
                        DO UPDATE SET
                            company_name = EXCLUDED.company_name,
                            market_cap = EXCLUDED.market_cap,
                            pe_ratio = EXCLUDED.pe_ratio,
                            pb_ratio = EXCLUDED.pb_ratio,
                            debt_to_equity = EXCLUDED.debt_to_equity,
                            roce = EXCLUDED.roce,
                            promoter_holding = EXCLUDED.promoter_holding,
                            eps_growth_3y = EXCLUDED.eps_growth_3y,
                            sales_growth_3y = EXCLUDED.sales_growth_3y,
                            is_survivor = EXCLUDED.is_survivor,
                            screen_date = EXCLUDED.screen_date,
                            updated_at = EXCLUDED.updated_at
                    """, (
                        row.get('ticker'),
                        row.get('company_name'),
                        row.get('market_cap'),
                        row.get('pe_ratio'),
                        row.get('pb_ratio'),
                        row.get('debt_to_equity'),
                        row.get('roce'),
                        row.get('promoter_holding'),
                        row.get('eps_growth_3y'),
                        row.get('sales_growth_3y'),
                        row.get('is_survivor', True),
                        row.get('screen_date'),
                        row.get('created_at'),
                        row.get('updated_at')
                    ))
                    count += 1
            
            db_connection.commit()
            logger.info(f"Upserted {count} records into screener_survivors table")
            return count
            
        except Exception as e:
            logger.error(f"Database upsert failed: {e}")
            db_connection.rollback()
            return 0


async def run_phase2(fo_tickers: Set[str] = None, db_connection=None) -> List[str]:
    """
    Execute Phase 2: Screener.in Fundamental Filtering.
    
    Args:
        fo_tickers: Set of F&O ticker symbols from Phase 1
        db_connection: Optional database connection
        
    Returns:
        List of survivor ticker symbols
    """
    logger.info("=" * 60)
    logger.info("PHASE 2: Screener.in Fundamental Filtering")
    logger.info("=" * 60)
    
    if not PLAYWRIGHT_AVAILABLE:
        logger.error("Phase 2 requires Playwright. Install with: pip install playwright && playwright install")
        return []
    
    downloader = ScreenerInDownloader()
    
    # Download from Screener.in
    df_raw = await downloader.download_screen_csv()
    
    if df_raw is None or df_raw.empty:
        logger.error("Phase 2 failed: Could not download from Screener.in")
        return []
    
    # Clean data
    df_clean = downloader.clean_screener_data(df_raw)
    
    # Intersect with F&O universe
    if fo_tickers:
        df_filtered = downloader.intersect_with_fo_universe(df_clean, fo_tickers)
    else:
        df_filtered = df_clean
        logger.warning("No F&O universe provided, returning all screener results")
    
    if df_filtered.empty:
        logger.error("Phase 2 failed: No stocks passed both screens")
        return []
    
    # Save to database if connection provided
    if db_connection:
        downloader.save_to_database(df_filtered, db_connection)
        tickers = df_filtered['ticker'].tolist()
    else:
        tickers = df_filtered['ticker'].tolist()
        logger.info(f"Returning {len(tickers)} survivor tickers (no database connection)")
    
    logger.info(f"Phase 2 complete: {len(tickers)} survivor stocks")
    logger.info("=" * 60)
    
    return tickers


if __name__ == "__main__":
    # Test run (requires Playwright installed and configured)
    print("Testing Phase 2 - Screener.in Downloader")
    print("Note: This requires Playwright to be installed: pip install playwright && playwright install")
    
    # Example usage with mock F&O tickers
    mock_fo_tickers = {'RELIANCE', 'TCS', 'INFY', 'HDFCBANK', 'ICICIBANK'}
    
    tickers = asyncio.run(run_phase2(fo_tickers=mock_fo_tickers))
    print(f"\nSurvivors: {tickers}")
