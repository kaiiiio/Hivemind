-- HIVEMIND TimescaleDB Schema
-- Layer 1: Data ingestion pipeline storage

-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- ============================================
-- MASTER TABLES
-- ============================================

-- F&O Universe master list (updated daily from NSE)
CREATE TABLE IF NOT EXISTS fo_universe (
    ticker VARCHAR(50) PRIMARY KEY,
    company_name VARCHAR(255),
    lot_size INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    added_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Screener.in fundamental survivors (updated weekly)
CREATE TABLE IF NOT EXISTS screener_survivors (
    ticker VARCHAR(50) PRIMARY KEY,
    company_name VARCHAR(255),
    market_cap NUMERIC,
    pe_ratio NUMERIC,
    pb_ratio NUMERIC,
    debt_to_equity NUMERIC,
    roce NUMERIC,
    promoter_holding NUMERIC,
    eps_growth_3y NUMERIC,
    sales_growth_3y NUMERIC,
    is_survivor BOOLEAN DEFAULT TRUE,
    screen_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- MARKET REGIME TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS market_regime (
    id SERIAL PRIMARY KEY,
    trade_date DATE UNIQUE NOT NULL,
    vix_close NUMERIC,
    vix_10d_avg NUMERIC,
    vix_percentile NUMERIC,
    fii_flow_10d_sum NUMERIC,
    dii_flow_10d_sum NUMERIC,
    nifty_change_pct NUMERIC,
    regime_status VARCHAR(20) CHECK (regime_status IN ('RISK_ON', 'RISK_OFF', 'CAUTIOUS')),
    regime_reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- DAILY PRICE DATA (Hypertable)
-- ============================================

CREATE TABLE IF NOT EXISTS daily_prices (
    time TIMESTAMPTZ NOT NULL,
    ticker VARCHAR(50) NOT NULL,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume BIGINT,
    adj_close NUMERIC,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Convert to hypertable for time-series optimization
SELECT create_hypertable('daily_prices', 'time', if_not_exists => TRUE);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_daily_prices_ticker ON daily_prices(ticker, time DESC);
CREATE INDEX IF NOT EXISTS idx_daily_prices_time ON daily_prices(time DESC);

-- ============================================
-- DELIVERY & OI DATA (Hypertable)
-- ============================================

CREATE TABLE IF NOT EXISTS delivery_data (
    time TIMESTAMPTZ NOT NULL,
    ticker VARCHAR(50) NOT NULL,
    deliverable_quantity BIGINT,
    total_quantity BIGINT,
    delivery_ratio NUMERIC,
    oi_change BIGINT,
    oi_open_interest BIGINT,
    fut_price_premium NUMERIC,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Convert to hypertable
SELECT create_hypertable('delivery_data', 'time', if_not_exists => TRUE);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_delivery_data_ticker ON delivery_data(ticker, time DESC);
CREATE INDEX IF NOT EXISTS idx_delivery_data_time ON delivery_data(time DESC);

-- ============================================
-- TRADE LOGS (for paper trading - Layer 4)
-- ============================================

CREATE TABLE IF NOT EXISTS trade_logs (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(50) NOT NULL,
    trade_type VARCHAR(10) CHECK (trade_type IN ('ENTRY', 'EXIT')),
    action VARCHAR(10) CHECK (action IN ('BUY', 'SELL')),
    quantity INTEGER,
    entry_price NUMERIC,
    exit_price NUMERIC,
    stop_loss NUMERIC,
    target_price NUMERIC,
    pnl NUMERIC,
    pnl_pct NUMERIC,
    trade_start_time TIMESTAMP WITH TIME ZONE,
    trade_end_time TIMESTAMP WITH TIME ZONE,
    strategy_signal_id VARCHAR(100),
    agent_consensus_score NUMERIC,
    market_regime_at_entry VARCHAR(20),
    status VARCHAR(20) DEFAULT 'OPEN' CHECK (status IN ('OPEN', 'CLOSED', 'STOPPED_OUT', 'TARGET_HIT')),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for trade analysis
CREATE INDEX IF NOT EXISTS idx_trade_logs_ticker ON trade_logs(ticker);
CREATE INDEX IF NOT EXISTS idx_trade_logs_status ON trade_logs(status);
CREATE INDEX IF NOT EXISTS idx_trade_logs_time ON trade_logs(trade_start_time DESC);

-- ============================================
-- AGENT OUTPUTS (Layer 2 - AI Swarm results)
-- ============================================

CREATE TABLE IF NOT EXISTS agent_outputs (
    id SERIAL PRIMARY KEY,
    run_date DATE NOT NULL,
    agent_name VARCHAR(50) NOT NULL,
    ticker VARCHAR(50),
    output_type VARCHAR(50),
    output_data JSONB,
    confidence_score NUMERIC,
    processing_time_ms INTEGER,
    model_used VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for agent performance tracking
CREATE INDEX IF NOT EXISTS idx_agent_outputs_run_date ON agent_outputs(run_date DESC);
CREATE INDEX IF NOT EXISTS idx_agent_outputs_agent ON agent_outputs(agent_name);

-- ============================================
-- FINAL TARGETS (Layer 3 - Aggregated signals)
-- ============================================

CREATE TABLE IF NOT EXISTS signal_targets (
    id SERIAL PRIMARY KEY,
    signal_date DATE NOT NULL,
    ticker VARCHAR(50) NOT NULL,
    rank INTEGER,
    entry_price NUMERIC,
    stop_loss NUMERIC,
    target_price NUMERIC,
    position_size_pct NUMERIC,
    trade_thesis TEXT,
    quant_score NUMERIC,
    news_sentiment_score NUMERIC,
    macro_regime VARCHAR(20),
    researcher_risk_note TEXT,
    orchestrator_decision VARCHAR(50),
    consensus_score NUMERIC,
    is_executed BOOLEAN DEFAULT FALSE,
    executed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for signal tracking
CREATE INDEX IF NOT EXISTS idx_signal_targets_date ON signal_targets(signal_date DESC);
CREATE INDEX IF NOT EXISTS idx_signal_targets_ticker ON signal_targets(ticker);

-- ============================================
-- FEEDBACK & LEARNING (Layer 5)
-- ============================================

CREATE TABLE IF NOT EXISTS trade_feedback (
    id SERIAL PRIMARY KEY,
    trade_log_id INTEGER REFERENCES trade_logs(id),
    ticker VARCHAR(50) NOT NULL,
    outcome VARCHAR(50),
    win_loss VARCHAR(10) CHECK (win_loss IN ('WIN', 'LOSS', 'BREAKEVEN')),
    r_multiple NUMERIC,
    which_agent_was_right VARCHAR(50),
    key_success_factors TEXT[],
    key_failure_factors TEXT[],
    entry_timing_score NUMERIC,
    exit_timing_score NUMERIC,
    lessons_learned TEXT,
    similar_historical_setups TEXT[],
    feedback_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Weekly tearsheet summary
CREATE TABLE IF NOT EXISTS weekly_tearsheets (
    id SERIAL PRIMARY KEY,
    week_start_date DATE NOT NULL,
    week_end_date DATE NOT NULL,
    total_trades INTEGER,
    wins INTEGER,
    losses INTEGER,
    win_rate NUMERIC,
    total_pnl NUMERIC,
    cagr NUMERIC,
    sharpe_ratio NUMERIC,
    max_drawdown NUMERIC,
    avg_r_multiple NUMERIC,
    best_trade_pct NUMERIC,
    worst_trade_pct NUMERIC,
    factor_attribution JSONB,
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- UTILITY FUNCTIONS
-- ============================================

-- Function to update updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply triggers to tables with updated_at
CREATE TRIGGER update_screener_survivors_updated_at
    BEFORE UPDATE ON screener_survivors
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_trade_logs_updated_at
    BEFORE UPDATE ON trade_logs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- INITIAL DATA SEED (optional)
-- ============================================

-- Insert a placeholder market regime record
INSERT INTO market_regime (trade_date, regime_status, regime_reason)
VALUES (CURRENT_DATE, 'CAUTIOUS', 'Initial setup - awaiting first data ingestion run')
ON CONFLICT (trade_date) DO NOTHING;
