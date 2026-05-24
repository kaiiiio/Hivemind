# HIVEMIND AI Layer Implementation Plan

## Short Explanation

The PDF describes a strong target system: five memory tiers, hybrid retrieval, seven specialist agents, a critic, an orchestrator, and a feedback loop. The best zero-cost way to build it is not to start with all seven agents. Start with reliable evidence capture, then add memory, then add agents.

The rule for every trade recommendation should be:

> No cited evidence, no trade recommendation.

## What We Should Build First

### Sprint 0: Event And Alert MVP

Build a market event pipeline before the full swarm:

1. Fetch free sources such as NSE/BSE/SEBI RSS or public pages where permitted.
2. Normalize each item into one `market_events` schema.
3. Deduplicate by hash.
4. Resolve tickers.
5. Classify event type with deterministic rules first.
6. Score alerts.
7. Store alerts in Postgres and optionally Redis.

This gives value immediately and gives NYSA/VERA real evidence later.

### Sprint 1: Free Local Memory Infrastructure

Use local Docker services:

1. TimescaleDB/Postgres: market data, procedures, outputs, events, alerts.
2. Redis: recent episodes and mistake logs.
3. Qdrant: long-term semantic memory.
4. Neo4j Community: graph relationships after enough clean events exist.

Qdrant Cloud is not mandatory. Local Qdrant is enough for paper trading and development.

### Sprint 2: Hybrid Retrieval

Implement retrieval in this order:

1. Postgres full-text search over `agent_outputs` and `market_events`.
2. RRF fusion.
3. Rule-based query expansion.
4. Local context compression.
5. Qdrant dense search only after embeddings are installed.
6. Neo4j graph search after graph data is populated.

This avoids making local model downloads a blocker.

### Sprint 3: Minimal Agent Loop

Start with:

1. `SENTINEL`: decides whether new events deserve attention.
2. `NYSA`: news/catalyst analyst.
3. `VERA`: critic/risk checker.
4. `APEX`: final paper-trade decision.

Add `VEGA`, `QUANTRA`, `LEXA`, and `SECTORA` after the alert pipeline and retrieval quality are stable.

## Improvements Over The PDF

1. Build market event ingestion before the full agent swarm.
2. Keep all model/provider choices configurable, not hardcoded.
3. Use local Qdrant instead of requiring Qdrant Cloud.
4. Avoid storing raw chain-of-thought. Store concise rationale, citations, uncertainties, and retrieval logs.
5. Use deterministic classifiers first, then add LLMs for ambiguous cases.
6. Add graceful degraded mode when Redis/Qdrant/Neo4j or LLM providers are offline.
7. Treat alerts and trades as separate states. News can trigger `WATCH`; it should not directly trigger `PROCEED`.

## Zero-Cost Performance Priorities

1. Batch database writes with conflict-safe indexes.
2. Cache recent episodes in Redis.
3. Use Postgres full-text search before paid/vector-heavy retrieval.
4. Run agents only for high-score events or nightly survivors.
5. Keep local rule-based fallback paths for query rewrite and compression.
6. Measure latency before adding rerankers or large embedding models.

## Implementation Started

This repo now has the first foundation pieces:

1. Docker services for Redis, Neo4j, and local Qdrant.
2. Database tables for procedural memory, market events, and alerts.
3. Unique indexes required by existing price/delivery upserts.
4. Memory Manager skeleton with Redis episodic fallback.
5. Agent output schemas.
6. RRF fusion.
7. Rule-based market event classifier and alert scoring.
8. Debate trigger helper.
9. Postgres full-text retrieval over `market_events` and `agent_outputs`.
10. Generic RSS connector that normalizes feed entries into `MarketEvent`.
11. Event repository and ingestion pipeline that scores/persists alerts.
12. Free/local CLI for RSS ingestion, alert review, and deterministic event triage.
13. First deterministic `SENTINEL -> NYSA -> VERA -> APEX` loop.
14. Deterministic triage output persistence into `agent_outputs`.
15. CLI review command for persisted agent outputs.

## Next Implementation Steps

1. Add source-specific RSS/feed configuration for NSE/BSE/SEBI-style feeds and improve ticker mapping.
2. Add a console/Streamlit alert view backed by the local Postgres tables.
3. Add Qdrant embedding support only after the basic retrieval tests pass.
4. Add Neo4j graph writer for confirmed events and paper decisions.
5. Add feedback writer that turns VERA vetoes and closed paper trades into mistake memory.

## Current Completion Estimate

The PDF's full AI layer is roughly 15-20% implemented.

Completed:

1. Sprint 0 foundation: schemas, deterministic event classification, scoring, event persistence path.
2. Sprint 1 foundation: local Redis/Qdrant/Neo4j/Postgres Docker plan and Redis fallback memory.
3. Sprint 2 foundation: query rewrite, RRF fusion, compression, and Postgres full-text retrieval.
4. First executable local event triage loop with schema-validated agent outputs.
5. Audit trail for deterministic agent outputs in Postgres.

Not complete yet:

1. Real source-specific RSS/feed configuration and ticker mapping quality.
2. Full 7-agent execution loop and debate orchestration.
3. Qdrant embedding collections and Neo4j graph writers.
4. Feedback/mistake learning beyond Redis storage primitives.
5. UI workflow for reviewing alerts and paper decisions.
