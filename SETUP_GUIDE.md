# HIVEMIND - Week 1 Data Ingestion Layer
## Setup & Testing Guide

This guide walks you through getting the data ingestion pipeline running locally.

---

## Step 1: Start TimescaleDB

```bash
cd /workspace
docker-compose up -d timescaledb
```

**Wait 30 seconds** for the database to initialize and run the schema migration.

Verify it's running:
```bash
docker-compose ps
# Should show: hivemind-timescaledb    Up (healthy)
```

Check database logs:
```bash
docker-compose logs timescaledb
```

---

## Step 2: Configure Environment

```bash
# Copy the template
cp config/.env.example config/.env

# Edit with your credentials (only SCREENER section needed for Week 1)
nano config/.env
```

**Required for Week 1:**
- Create free account at [screener.in](https://www.screener.in)
- Build a custom screen with your fundamental filters
- Copy your screen URL into `.env`

Example Screener.in screen URL:
```
SCREENER_SCREEN_URL=https://www.screener.in/screen/custom/1234567/
```

**Database defaults work with docker-compose:**
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=hivemind
DB_USER=hivemind
DB_PASSWORD=hivemind_password
```

---

## Step 3: Install Python Dependencies

```bash
cd /workspace
pip install -r requirements.txt
```

**Install Playwright browsers:**
```bash
playwright install chromium
```

---

## Step 4: Test Individual Phases

### Test Phase 1: F&O Universe

```bash
cd /workspace/src
python data_ingestion/nse_universe_fetcher.py
```

Expected output:
```
=========================================
PHASE 1: F&O Universe Definition
=========================================
INFO: Downloading F&O market lots from https://www.nseindia.com...
INFO: Saved F&O market lots to /workspace/data/fo_mktlots_20250107_183000.csv (185 records)
INFO: Cleaned F&O universe: 185 valid tickers
INFO: Phase 1 complete: 185 F&O tickers available
```

### Test Phase 3: Market Regime

```bash
python data_ingestion/market_regime_checker.py
```

Expected output:
```
=========================================
PHASE 3: Market Regime Assessment
=========================================
INFO: Downloading India VIX data...
INFO: Downloaded 60 days of VIX data
INFO: VIX Close: 12.45, 10d Avg: 12.89, Percentile: 35.0
INFO: REGIME DECISION: RISK_ON - All indicators favorable
```

### Test Phase 6: Database Connection

```bash
python data_ingestion/database_upsert.py
```

Expected output:
```
INFO: Connected to database: hivemind@localhost
Database connection successful!
```

---

## Step 5: Run Full Pipeline

```bash
cd /workspace/src
python data_ingestion/master_pipeline.py
```

**What this does:**
1. Downloads F&O universe from NSE (~185 stocks)
2. Logs into Screener.in and exports fundamental survivors (~30-50 stocks)
3. Checks market regime (VIX, FII/DII flows)
4. Downloads Bhavcopy data (delivery %, OI changes)
5. Downloads 250 days OHLCV from yfinance
6. Upserts everything into TimescaleDB

**Expected duration:** 2-5 minutes (depends on internet speed)

---

## Step 6: Verify Data in Database

Connect to TimescaleDB:
```bash
docker exec -it hivemind-timescaledb psql -U hivemind -d hivemind
```

Query F&O universe:
```sql
SELECT COUNT(*) as fo_count FROM fo_universe WHERE is_active = TRUE;
-- Expected: ~185
```

Query survivors:
```sql
SELECT COUNT(*) as survivor_count FROM screener_survivors WHERE is_survivor = TRUE;
-- Expected: 30-50 (or 0 if Screener.in not configured)
```

Query daily prices:
```sql
SELECT ticker, time, close 
FROM daily_prices 
WHERE ticker IN ('RELIANCE', 'TCS', 'INFY') 
ORDER BY time DESC 
LIMIT 10;
```

Check market regime:
```sql
SELECT trade_date, regime_status, vix_close, regime_reason 
FROM market_regime 
ORDER BY trade_date DESC 
LIMIT 5;
```

Exit psql:
```sql
\q
```

---

## Troubleshooting

### Phase 1 fails (NSE download)
**Error:** `Failed to download F&O market lots`

**Solution:**
- NSE has rate limits; wait 5 minutes
- Check your internet connection
- The script uses proper headers but NSE can be unpredictable

### Phase 2 fails (Screener.in)
**Error:** `Login failed` or `Export button not found`

**Solution:**
1. Verify credentials in `.env`
2. Test login manually in browser
3. Ensure your custom screen URL works
4. Try with `headless=False` in screener_fundamentals.py for debugging

### Phase 3 fails (yfinance)
**Error:** `No VIX data received`

**Solution:**
- yfinance occasionally rate limits
- Wait 1-2 minutes and retry
- Check if `^INDIAVIX` works: `yfinance.Ticker("^INDIAVIX").history(period='1d')`

### Database connection fails
**Error:** `Connection refused`

**Solution:**
```bash
# Check if container is running
docker-compose ps

# Restart if needed
docker-compose restart timescaledb

# Check logs
docker-compose logs timescaledb
```

### Port 5432 already in use
**Error:** `Bind for 0.0.0.0:5432 failed: port is already allocated`

**Solution:**
Either stop your local PostgreSQL:
```bash
sudo systemctl stop postgresql
```

Or change the port in `docker-compose.yml`:
```yaml
ports:
  - "5433:5432"  # Use 5433 externally
```

Then update `.env`:
```
DB_PORT=5433
```

---

## Cron Setup (Production)

To run daily at 18:30 IST:

```bash
crontab -e
```

Add this line:
```
30 18 * * * cd /workspace && /usr/bin/python3 src/data_ingestion/master_pipeline.py >> /workspace/logs/cron.log 2>&1
```

**Test cron logging:**
```bash
tail -f /workspace/logs/cron.log
```

---

## Next Steps (Week 2)

With data flowing into TimescaleDB, we'll build:

1. **Null-Beta Quant Engine** - 7-parameter scoring system
   - Monthly/quarterly/annual lookbacks
   - Momentum, quality, volatility factors
   - Ranked stock lists

2. **Backtesting Framework** - Validate against historical data
   - Walk-forward analysis
   - Factor attribution
   - Performance metrics

Ready to proceed to Week 2?

---

## Quick Reference

**Start database:**
```bash
docker-compose up -d timescaledb
```

**Stop database:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f timescaledb
```

**Run pipeline:**
```bash
cd /workspace/src && python data_ingestion/master_pipeline.py
```

**Connect to DB:**
```bash
docker exec -it hivemind-timescaledb psql -U hivemind -d hivemind
```

**Clear cache/data:**
```bash
rm -rf /workspace/data/* /workspace/logs/*
```
