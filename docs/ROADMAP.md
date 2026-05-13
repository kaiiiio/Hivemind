# Hivemind Roadmap

This document outlines the development phases, current status, and future plans for the Hivemind Multi-Agent AI Trading System.

## Current Status

### Week 1: Data Ingestion Layer ✓ COMPLETE
The foundation of the system is built, focusing on high-quality data acquisition and storage.

- **Phase 1: Universe Fetching**
  - `nse_universe_fetcher.py`: Downloads official F&O constituent list (~185 stocks) from NSE.
- **Phase 2: Fundamental Analysis**
  - `screener_fundamentals.py`: Playwright automation for Screener.in exports (Valuation, Solvency, Efficiency metrics).
- **Phase 3: Market Regime Detection**
  - `market_regime_checker.py`: VIX percentile + FII/DII flow analysis to understand the broader market context.
- **Phase 4: Price Microstructure**
  - `price_microstructure_loader.py`: Combines Bhavcopy delivery data with yfinance OHLCV for a granular view.
- **Phase 5: Centralized Storage**
  - `database_upsert.py`: Robust TimescaleDB hypertable upserts with conflict handling.
- **Phase 6: Orchestration**
  - `master_pipeline.py`: Main orchestrator that sequences all phases.

---

## Future Roadmap

### Phase 2: Signal Generation (In Progress)
- [ ] Implement technical indicator agent.
- [ ] Develop sentiment analysis agent for news and social media.
- [ ] Build a "Debate Protocol" for agent consensus.

### Phase 3: Execution & Risk Management
- [ ] Broker API integration.
- [ ] Position sizing logic based on conviction levels.
- [ ] Real-time stop-loss and trailing-profit monitoring.

### Phase 4: Feedback & Learning
- [ ] Post-trade analysis agent to review successes and failures.
- [ ] Vector-based memory for agents to "remember" market conditions.
