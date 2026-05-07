# HIVEMIND - Multi-Agent AI Trading System

## Overview

HIVEMIND is a swarm-based AI trading system that wraps quantitative signal generation inside a multi-agent consensus framework. Unlike traditional signal engines, HIVEMIND uses specialized AI agents that debate, research, remember, and learn from each trade.

## Quick Start

### Step 1: Setup Environment

```bash
cd /workspace
cp config/.env.example config/.env
# Edit config/.env with your credentials
```

### Step 2: Start Database

```bash
docker-compose up -d timescaledb
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Test Data Ingestion

```bash
cd src && python data_ingestion/master_pipeline.py
```

## Current Status

**Week 1: Data Ingestion Layer** ✓ COMPLETE

All 6 phases implemented:
- Phase 1: F&O Universe (NSE)
- Phase 2: Screener.in (Playwright)
- Phase 3: Market Regime (VIX, FII/DII)
- Phase 4-5: Bhavcopy & OHLCV
- Phase 6: TimescaleDB Upsert

See full documentation in the project files.

## License

MIT License - Educational purposes only. Not financial advice.
