# HIVEMIND Documentation Index

HIVEMIND is an AI-swarm capital-markets intelligence terminal for Indian markets.

It is not a single-asset screener or news scraper. The end product is a professional market terminal for situations forming across shares/equities, debt, commodities, FX, rates, derivatives for hedging, macro policy, tenders, flows, and price action, then explaining them with evidence.

## Canonical Documents

| Document | What It Owns |
|---|---|
| [Architecture](./architecture.md) | Full system theory: cross-asset market mesh, swarm-first pipelines, situation engines, event graph, roadmap. |
| [Data Foundation](./data-foundation.md) | Source strategy, market-data vendor plan, ingestion swarms, storage model, freshness tiers, first build sequence. |
| [AI Layer](./ai-layer.md) | Model-agnostic agents, swarm routing, token optimization, graph/RAG memory, reasoning and critique protocols. |
| [Research Basis](./research-basis.md) | Research papers, vendor findings, quant methods, AI techniques, and decisions adopted into the architecture. |

No separate DOCX/PDF specs are maintained. Markdown is the source of truth for developers.

## Core Thesis

Markets do not move as one clean signal. They move as situations:

```text
event + materiality + company exposure + sector context + market behavior + macro/flow regime + valuation + evidence quality
```

HIVEMIND turns those fragments into evidence-cited situation briefs.

## End Product

HIVEMIND Terminal is the investor-facing product.

It should feel like a serious market terminal, not a chat app:

- universal search for issuers, securities, sectors, themes, commodities, currencies, rates, derivatives, policies, and situations
- situation monitor ranked by materiality, evidence quality, market confirmation, valuation, and freshness
- company/security pages with filings, price/delivery history, valuation, peers, catalysts, and risks
- cross-asset pages for crude, metals, rates, FX, debt/credit, derivatives, index flows, and policy shocks
- evidence explorer with raw source lineage and timestamps
- agent analysis panel showing consensus, uncertainty, and missing evidence
- watchlists, alerts, research queue, and post-mortem tracking

The pitch is:

```text
professional capital-markets workflow + AI agent research + cross-asset evidence graph
```

Bloomberg is the reference point for seriousness and workflow integration. HIVEMIND's differentiation is not copying Bloomberg. It is building an agentic intelligence layer for fragmented Indian capital-market situations.

## Market Scope

Mandatory coverage:

- NSE and BSE mainboard equities
- BSE-exclusive names
- full equity breadth across listed issuers, with depth beyond the obvious liquid universe
- listed and liquid debt/rates context where available
- sector and theme baskets
- commodities and metals
- rates, bond yields, FX, crude, gas, and global risk context
- derivatives context for hedging, especially futures/options availability, basis, and risk offsets
- market-structure events such as MSCI, FTSE, Nifty/BSE index changes, F&O inclusion, surveillance, block/bulk deals

Optional after the base pipeline:

- NSE SME and BSE SME
- deeper options analytics
- higher-frequency intraday feeds

## Build Order

1. Build the evidence-first data foundation.
2. Backfill historical price, delivery, filings, debt/rates, commodities, FX, derivatives context, macro, flow, and policy data so every signal can be replayed.
3. Add deterministic event, price, credit/rates, commodity, FX, macro, tender, valuation, hedge, and market-structure features.
4. Add the ingestion swarm to improve parsing, entity resolution, source monitoring, and missed-event audits.
5. Add situation engines that create specific, explainable candidates.
6. Add model-agnostic AI swarms for research, risk review, quant validation, and final synthesis.
7. Scale from 10-15 core agents/workers to 30-40 specialists through routing, not by running every agent on everything.

## Non-Negotiables

- AI is not the market data source.
- The terminal is the product; the swarm is the intelligence layer behind every screen.
- Search engines are discovery and audit tools, not truth.
- Historical data is first-class. Live data catches now; history proves early, late, noisy, or useful.
- The product scope is capital markets. Shares are one lane; debt, commodities, FX, rates, and derivatives matter for risk and hedging.
- Every important output must cite evidence IDs and source timestamps.
- Every event must be replayable from raw evidence.
- Complex prompts become research jobs with source plans, agent plans, hard filters, debate, synthesis, memory writeback, and outcome tracking.
- User notes and AI outputs are knowledge artifacts, not verified facts, until tied to evidence.
- Raw evidence, parsed records, feature stores, vector memory, graph memory, agent runs, and outcome memory are separate layers.
- Vector stores and graphs are indexes/reasoning structures over evidence, not replacements for the evidence archive.
- Stored knowledge makes the system smarter through retrieval, routing, critique, thresholds, and post-mortems before any fine-tuning.
- Equity breadth matters, but it is only one lane in a wider capital-markets system.
- Scores are situation-specific. Do not build one generic market score as the product.

## Situation Families

| Example Observation | HIVEMIND Situation Family |
|---|---|
| Large order win relative to company size | material order-win re-rating |
| Strategic manufacturing theme gaining attention | theme-led strategic manufacturing re-rating |
| Price moving before visible news | unexplained accumulation investigation |
| Budget/policy/tender wave affecting suppliers | policy and procurement tailwind |
| Results plus breakout | earnings re-rating with market confirmation |
| MSCI/index/F&O change | market-structure flow event |
| Crude, FX, metals, geopolitical, or rate shock | macro shock transmission event |
| Catalyst with stretched or cheap valuation | valuation repricing context |
