# Architecture Overview

Hivemind is designed as a modular, swarm-based AI trading system. It separates concerns into clear layers: Data, Intelligence, and Execution.

## System Components

### 1. Data Ingestion Layer (`src/data_ingestion/`)
This layer is responsible for gathering all raw signals needed for the agents to make decisions.
- **NSE Universe Fetcher**: Maintains the scope of tradable instruments.
- **Fundamental Scraper**: Extracts financial health metrics.
- **Regime Checker**: Analyzes macro-market conditions (VIX, FII/DII flows).
- **Price Microstructure**: Captures OHLCV and delivery data.

### 2. Database Layer (`database/`)
- **TimescaleDB**: Used for storing time-series market data.
- **Hypertables**: Data is automatically partitioned by time for high-performance querying and storage.
- **Schema Management**: Handles tables for `market_regimes`, `stock_fundamentals`, and `price_data`.

### 3. Orchestration Layer
- **Master Pipeline**: Coordinates the sequence of data ingestion to ensure dependencies are met (e.g., fetching the universe before scraping fundamentals).

### 4. Utilities (`src/utils/`)
- Common logging, database connection management, and shared configuration loaders.

## Multi-Agent Framework (Conceptual)
Hivemind will eventually implement a multi-agent debate protocol where:
- **Research Agents** pull data from the Ingestion layer.
- **Debate Agents** argue for/against trades based on specific domains (Technical vs. Fundamental).
- **Consensus Agent** finalizes the trade decision based on weighted conviction.

## Data Flow
1. **Fetch**: `master_pipeline.py` triggers specialized scripts.
2. **Transform**: Data is cleaned and normalized into a standard format.
3. **Upsert**: `database_upsert.py` pushes data into TimescaleDB.
4. **Query**: Agents query the database to retrieve historical and real-time state.
