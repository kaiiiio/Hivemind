# HIVEMIND AI Layer Review + Market News Alerts Plan

## Short Verdict

The AI layer design is strong conceptually, but it is overbuilt before the most important production primitive exists:

> reliable, timestamped, deduplicated, source-ranked market event ingestion.

If HIVEMIND needs to detect better opportunities, the system should not start with 7 agents. It should start with a high-quality event pipeline that tells the agents what changed, when it changed, where it came from, and whether it matters.

## Current Spec Strengths

- The LLM is correctly treated as a reasoning layer, not a database.
- The 5-tier memory system is a good mental model.
- Hybrid retrieval is the right direction: keyword + vector + graph.
- VERA as a critic is useful and should stay.
- The post-mortem loop is one of the best parts of the design.
- Pydantic output validation is essential.
- The insistence on citation-backed recommendations is correct.

## Biggest Missing Piece

The spec has memory and agents, but not enough about incoming data.

For trading/alerts, this is the real heartbeat:

```text
Market / News / Filing Sources
      |
      v
Ingestion Connectors
      |
      v
Normalizer + Deduper
      |
      v
Entity Resolver
      |
      v
Event Classifier
      |
      v
Alert Scoring Engine
      |
      +--> Dashboard / Telegram / Email
      +--> Redis recent events
      +--> Postgres audit log
      +--> Qdrant semantic memory
      +--> Neo4j event graph
      +--> Agent swarm
```

Without this layer, agents will depend on whatever context happens to be retrieved, which is dangerous.

## What To Add Before The Agent Swarm

### 1. Market Event Ingestion Layer

Create a new module:

```text
hivemind/
  ingestion/
    sources/
      nse_rss.py
      sebi_rss.py
      bse_filings.py
      newsapi.py
      gdelt.py
      alphavantage.py
    normalizer.py
    deduper.py
    entity_resolver.py
    pdf_extractor.py
    scheduler.py
```

This layer should run every 1-5 minutes during market hours and every 15-30 minutes outside market hours.

### 2. Source Priority Model

Not every source should be trusted equally.

Suggested ranking:

| Rank | Source Type | Example | Trust |
| --- | --- | --- | --- |
| 1 | Official exchange filing | NSE/BSE corporate announcement | Highest |
| 2 | Regulator source | SEBI/RBI circular | Highest |
| 3 | Company IR page | investor presentation, press release | High |
| 4 | Reputed financial news | business news source | Medium |
| 5 | Aggregator/API | NewsAPI, GDELT, Alpha Vantage | Medium |
| 6 | Social media | X, Telegram, Reddit | Low, alert only |

Rule:

> Unofficial news can trigger an alert, but official confirmation should be required before trade recommendation.

### 3. Event Schema

Every incoming item should be normalized into one shape.

```python
MarketEvent = {
    "event_id": str,
    "source": str,
    "source_type": "EXCHANGE" | "REGULATOR" | "NEWS" | "COMPANY" | "SOCIAL",
    "source_url": str,
    "published_at": datetime,
    "fetched_at": datetime,
    "tickers": list[str],
    "company_names": list[str],
    "sector": str | None,
    "event_type": str,
    "headline": str,
    "summary": str,
    "raw_text": str,
    "document_url": str | None,
    "severity": float,
    "sentiment": float,
    "confidence": float,
    "requires_confirmation": bool,
    "dedupe_hash": str,
}
```

### 4. Event Types To Detect

Start with rule-based tags first. Add LLM classification later.

High-signal event types:

- `RESULTS`
- `EARNINGS_BEAT`
- `EARNINGS_MISS`
- `GUIDANCE_CHANGE`
- `ORDER_WIN`
- `CAPEX`
- `MERGER_ACQUISITION`
- `DEMERGER`
- `BLOCK_DEAL`
- `PROMOTER_BUY`
- `PROMOTER_SELL`
- `PLEDGE`
- `PLEDGE_RELEASE`
- `MANAGEMENT_CHANGE`
- `AUDITOR_RESIGNATION`
- `CREDIT_RATING_UPGRADE`
- `CREDIT_RATING_DOWNGRADE`
- `REGULATORY_ACTION`
- `USFDA_ALERT`
- `LITIGATION`
- `FUNDRAISING`
- `BUYBACK`
- `DIVIDEND`
- `SPLIT_BONUS`
- `INSIDER_TRADING_DISCLOSURE`
- `RELATED_PARTY_TRANSACTION`

### 5. Alert Scoring

Every event should get an alert score.

```text
alert_score =
  source_trust_score * 0.30
  + event_severity * 0.25
  + ticker_relevance * 0.15
  + price_volume_confirmation * 0.15
  + novelty_score * 0.10
  + agent_interest_score * 0.05
```

Example:

```text
NSE filing + auditor resignation + stock down 4% on volume spike
  = critical alert

News article says "possible order win" but no exchange filing
  = watch alert, needs confirmation
```

## Recommended Alert Flow

```text
New event arrives
  |
  v
Is it duplicate?
  |
  +-- yes -> update existing event, do not alert again
  |
  +-- no
       |
       v
Resolve ticker/company
       |
       v
Classify event type
       |
       v
Score severity + source trust
       |
       v
Check price/volume confirmation
       |
       v
Create alert
       |
       +--> low: store only
       +--> medium: dashboard
       +--> high: dashboard + notification
       +--> critical: notification + trigger VERA/NYSA immediately
```

## Agent System Improvements

### 1. Do Not Store Chain Of Thought

The current spec includes:

```python
"reasoning_steps": []
```

Better:

```python
"decision_rationale": [],
"evidence_citations": [],
"uncertainties": [],
"retrieval_log": [],
```

Store concise rationales and cited evidence, not raw chain-of-thought.

### 2. Add A Dedicated Event Sentinel Agent

Before VEGA/NYSA/QUANTRA/LEXA/SECTORA, add one lightweight agent:

```text
SENTINEL - Event Triage Agent
```

Job:

- read fresh events
- classify urgency
- decide whether the full swarm should run now
- suppress low-value noise
- escalate critical events immediately

This avoids spending 7-agent swarm calls on every tiny update.

### 3. Add A Data Quality Agent

Add:

```text
AUDIT - Data Quality Agent
```

Job:

- detect stale data
- detect missing prices
- detect broken RSS/API feeds
- detect timestamp mismatch
- detect suspicious duplicate filings
- block trading decisions when source coverage is incomplete

For markets, bad data is worse than no AI.

### 4. Make Agent Models Configurable

The spec hardcodes model choices. That will age badly.

Use:

```yaml
agents:
  nysa:
    provider: groq
    model: llama-current-fast
    fallback_provider: openai
    fallback_model: small-reasoning-model
```

Do not bake provider limits or model names into the architecture.

### 5. Add Provider Health Checks

Before nightly run:

```text
Check provider status
  |
  +-- Gemini reachable?
  +-- Groq reachable?
  +-- embedding model loaded?
  +-- Qdrant reachable?
  +-- Redis reachable?
  +-- Neo4j reachable?
  +-- Postgres reachable?
```

If any critical dependency fails, downgrade to a smaller workflow or skip recommendations.

### 6. Separate "Alert" From "Trade"

Important:

```text
Alert != recommendation
News != trade
AI thesis != execution
```

Recommended states:

```text
INFO
WATCH
INVESTIGATE
HIGH_ALERT
TRADE_CANDIDATE
APPROVED_PAPER_TRADE
BLOCKED
```

## News And Alert Sources

### Minimum Free/Low-Cost Stack

Use this first:

1. NSE RSS feeds for corporate information and filings.
2. SEBI RSS for circulars, press releases, orders, and rulings.
3. BSE corporate announcements page/API if access is stable.
4. Company investor relations pages for tracked tickers.
5. GDELT for broad web/news monitoring.
6. NewsAPI or Alpha Vantage for additional news coverage.
7. Screener-style pages only for manual reference unless terms allow automated use.

### More Reliable Paid/Official Stack

Use this when serious:

1. NSE paid corporate data feed.
2. Licensed BSE/NSE data vendor.
3. Broker market-data API.
4. Paid news feed if latency matters.

Free sources are okay for learning and paper trading. For real money, source licensing and latency matter.

## Suggested Database Additions

### PostgreSQL Tables

```sql
CREATE TABLE market_events (
    event_id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    source_type TEXT NOT NULL,
    source_url TEXT,
    published_at TIMESTAMPTZ NOT NULL,
    fetched_at TIMESTAMPTZ NOT NULL,
    tickers TEXT[] NOT NULL DEFAULT '{}',
    sector TEXT,
    event_type TEXT NOT NULL,
    headline TEXT NOT NULL,
    summary TEXT,
    raw_text TEXT,
    document_url TEXT,
    severity NUMERIC NOT NULL,
    sentiment NUMERIC,
    confidence NUMERIC NOT NULL,
    requires_confirmation BOOLEAN NOT NULL DEFAULT FALSE,
    dedupe_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_market_events_tickers ON market_events USING gin(tickers);
CREATE INDEX idx_market_events_published_at ON market_events(published_at DESC);
CREATE INDEX idx_market_events_type ON market_events(event_type);
CREATE UNIQUE INDEX idx_market_events_dedupe ON market_events(dedupe_hash);
```

```sql
CREATE TABLE alerts (
    alert_id TEXT PRIMARY KEY,
    event_id TEXT REFERENCES market_events(event_id),
    ticker TEXT,
    alert_level TEXT NOT NULL,
    alert_score NUMERIC NOT NULL,
    reason TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'OPEN',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    acknowledged_at TIMESTAMPTZ
);
```

### Redis Keys

```text
events:latest                      -> sorted set by timestamp
events:ticker:{ticker}             -> sorted set
alerts:open                        -> sorted set by score
source:health:{source_name}        -> hash
dedupe:seen:{dedupe_hash}          -> string TTL 7 days
```

### Qdrant Collection

Add:

```text
market_events
```

Payload:

```text
ticker, sector, event_type, source, published_at, severity, sentiment, confidence
```

### Neo4j Additions

Add:

```text
(:Source {name, type, trust_score})
(:Alert {alert_id, level, score})

(:Source)-[:PUBLISHED]->(:NewsEvent)
(:NewsEvent)-[:MENTIONS]->(:Stock)
(:NewsEvent)-[:TRIGGERED_ALERT]->(:Alert)
(:Alert)-[:REVIEWED_BY]->(:Agent)
```

## Revised Sprint Order

The current sprint plan starts with memory infra. I would add a new Sprint 0 before it.

### Sprint 0: News + Event Ingestion MVP

Build:

- NSE RSS connector
- SEBI RSS connector
- generic RSS connector
- normalizer
- deduper
- ticker resolver
- event classifier
- alert scorer
- Postgres event tables
- simple Streamlit alert dashboard

Acceptance criteria:

- can fetch latest filings/news
- can identify ticker/company
- can classify at least 15 event types
- can dedupe repeated articles
- can show latest alerts in dashboard
- can send high-severity alerts to console/Telegram/email

Only after this should you build the larger swarm.

## Best MVP Architecture

For the first working version:

```text
RSS/API Pollers
  |
  v
Postgres market_events
  |
  v
Rule-based classifier
  |
  v
Alert scorer
  |
  +--> Streamlit dashboard
  +--> Redis latest alerts
  +--> NYSA summary when score > threshold
```

Avoid starting with:

- 7 agents
- Neo4j graph
- procedural memory
- automatic weight optimization
- full post-mortem learning

Those are powerful, but they need clean event data first.

## Practical Build Order

1. Build event ingestion.
2. Build alert dashboard.
3. Add simple NYSA news analyst.
4. Add retrieval over stored events.
5. Add VERA critic.
6. Add APEX decision maker.
7. Add Qdrant memory.
8. Add Neo4j graph.
9. Add post-mortems.
10. Add full 7-agent swarm.

This gives you value every week instead of waiting months.

## Key Risks In Current Spec

### Too Much Complexity Too Early

Seven agents, five memory tiers, graph RAG, reranking, compression, feedback learning, and optimization is a lot for one full-stack engineer.

Start smaller:

```text
SENTINEL -> NYSA -> VERA -> APEX
```

Then expand.

### Free-Tier Assumptions

Provider limits and model availability change often. Treat all limits as config, not architecture.

### Latency Target May Be Unrealistic

The spec says full hybrid retrieval with rewrite, parallel retrieval, rerank, and compression should complete under 2 seconds. That may be tight on a local machine, especially with local cross-encoder reranking.

Track:

- p50 latency
- p95 latency
- p99 latency
- timeout rate
- degraded-mode usage

### Graph Is Useful, But Not First

Neo4j is powerful after you have many clean events and decisions. Early graph data will be sparse.

Use Postgres first, graph second.

### LLM-Based Compression Can Lose Critical Facts

For market filings, compression must preserve numbers.

Use extraction rules for:

- order value
- revenue
- profit
- margin
- date
- record date
- promoter percentage
- pledge percentage
- rating change
- management name

Then let the LLM summarize only after numbers are extracted.

## Final Recommended System Shape

```text
                  Data Sources
        NSE RSS | SEBI RSS | BSE | News APIs | Company IR
                         |
                         v
              Event Ingestion Pipeline
                         |
                         v
      Normalize -> Dedupe -> Resolve Ticker -> Classify
                         |
                         v
                  Alert Scoring
                         |
             +-----------+-----------+
             |                       |
             v                       v
      Alert Dashboard           Memory Stores
                                     |
                                     v
                              AI Agent Layer
                         SENTINEL -> NYSA -> VERA -> APEX
                                     |
                                     v
                              Paper Trade Queue
                                     |
                                     v
                              Post-Mortem Loop
```

## One-Line Product Definition

HIVEMIND should first become:

> a market event detection and alerting engine that uses AI to explain which events matter, why they matter, and what evidence supports the alert.

Then it can become a trade-decision swarm.

