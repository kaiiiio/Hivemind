# HIVEMIND Documentation Index

HIVEMIND is an evidence-first market intelligence system for Indian equities, focused on small and mid caps, swing-trading setups, and missed catalyst detection.

The documentation is organized into three canonical files:

| Document | Purpose |
|---|---|
| [Architecture](./architecture.md) | Explains the full market intelligence architecture: evidence graph, situation engines, search lane, model-agnostic AI swarm, and final alert philosophy. |
| [Data Foundation](./data-foundation.md) | Defines the ingestion backbone: sources, storage model, source priority, event taxonomy, processing lanes, sprint plan, and first build sequence. |
| [AI Layer](./ai-layer.md) | Defines the AI reasoning layer: memory, retrieval, agent roles, critic behavior, and model-agnostic execution boundary. |

## Build Order

1. Build the data foundation first.
2. Add situation engines on top of structured events and price/volume behavior.
3. Fuse the model-agnostic AI swarm after raw evidence and situation candidates exist.
4. Use search engines only as a triggered investigation and audit layer, not as the primary truth source.

## Core Rule

AI is not the market data source.

AI reads evidence, extracts structure, maps context, challenges assumptions, and writes situation briefs. The raw evidence store remains the source of truth.

