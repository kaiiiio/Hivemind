# HIVEMIND Functional MVP Grant Budget

Date: 2026-06-09  
Grant target: INR 2,00,000  
Scope: functional MVP with 10-15 model-agnostic agents for Indian capital-markets intelligence  
Budget period: 90 days from grant approval

## Important Positioning

This budget is intentionally grant-defensible, not fake-inflated.

The right way to make the ask stronger is to include real buffers:

- paid market-data/vendor pilot reserve
- API and search overage reserve
- storage/backfill reserve
- evaluation and QA reserve
- contingency for source changes, parser failures, and model-provider changes

Do not claim invented vendor quotes. For exchange/vendor market data, use a reserve until an authorized quote is obtained.

## MVP Outcome

The grant funds a working prototype of HIVEMIND as an AI-swarm capital-markets intelligence terminal.

The MVP should demonstrate:

1. Data ingestion from official and public sources.
2. Historical price/delivery/event backfill.
3. Raw evidence storage with evidence IDs.
4. Parsed records for filings, market data, policy/tender items, and research notes.
5. Feature generation for price action, valuation, liquidity, market structure, and event windows.
6. Graph memory connecting companies, sectors, policies, tenders, commodities, rates, FX, and events.
7. 10-15 model-agnostic agents.
8. Situation engines for early MVP use cases.
9. Deep-research workflow orchestration.
10. Basic backtesting/replay loop.
11. Web terminal prototype with search, situations, evidence view, and agent traces.

## MVP Agent Set

The first MVP does not need 40 agents. It needs a strong routed core.

| # | Agent / Worker | Purpose |
|---|---|---|
| 1 | Source Health Agent | monitors source failures, schema drift, blocked pages, freshness gaps |
| 2 | Evidence Intake Agent | classifies and stores raw evidence before analysis |
| 3 | Filing Parser Agent | extracts order values, dates, customers, tables, risk text, and corporate fields |
| 4 | Entity Resolver Agent | maps names, aliases, symbols, BSE/NSE codes, ISINs, ministries, customers |
| 5 | Market Data Worker | builds OHLCV, delivery, liquidity, return, and event-window features |
| 6 | Macro / Policy Agent | maps RBI, SEBI, MoSPI, PIB, budget, ministry, and regulator items to sectors |
| 7 | Tender / Procurement Agent | parses tender/procurement evidence and maps it to listed suppliers |
| 8 | Search Investigator Agent | runs targeted search, finds missing context, and grades source quality |
| 9 | Graph Builder Agent | writes company-sector-policy-tender-commodity-event relationships |
| 10 | Price / Volume Agent | interprets price confirmation, accumulation, delivery, gaps, and liquidity risk |
| 11 | Valuation Agent | checks valuation, history, peer context, and whether catalyst is priced in |
| 12 | Quant Validator Agent | runs event-study, abnormal-return, and false-positive checks |
| 13 | Bull Case Agent | constructs the strongest evidence-backed positive thesis |
| 14 | Risk Review Agent | attacks the thesis, rejects weak evidence, and flags traps |
| 15 | Synthesis Agent | publishes final situation brief with evidence, uncertainty, and follow-up questions |

## Costing Assumptions

| Assumption | Value Used |
|---|---|
| Budget duration | 90 days |
| USD/INR conversion | approximately INR 95.6 per USD, based on live public FX pages on 2026-06-09 |
| GST / payment / FX buffer | 10-18% where applicable |
| LLM strategy | model-agnostic routing across DeepSeek, Qwen, Gemini/OpenAI if needed |
| Data strategy | free/public/official first, paid vendor reserve for gaps |
| Hosting strategy | lean VPS + managed DB or Supabase, Vercel for investor/terminal frontend |
| Developer salary | not included in cash budget; founder/dev effort treated as in-kind contribution |

## Realistic 90-Day Grant Budget

This is the recommended INR 2,00,000 budget for a functional MVP.

| Category | Grant Budget | Why It Is Needed |
|---|---:|---|
| 1. Market data and evidence acquisition reserve | 45,000 | paid data/API pilot, exchange/vendor quote buffer, historical gaps, fallback data procurement |
| 2. AI model/API credits | 35,000 | 10-15 agents, extraction, summarization, routing, debate, synthesis, search-assisted research |
| 3. Cloud compute and workers | 28,000 | API backend, ingestion workers, scheduled jobs, parser jobs, queue workers |
| 4. Database, vector, graph, and storage | 22,000 | Postgres/pgvector or Supabase, object storage, graph DB trial, backups, evidence archive |
| 5. Search/news/research tooling | 14,000 | search API credits or crawling infrastructure, RSS monitoring, source snapshots |
| 6. Backtesting and evaluation infrastructure | 16,000 | event-study compute, historical replay jobs, false-positive tracking, benchmark datasets |
| 7. Observability, security, backups | 12,000 | logging, error tracking, uptime checks, snapshot backups, secrets hygiene |
| 8. Frontend hosting, domain, deployment | 8,000 | Vercel Pro or equivalent, domain, deployment previews, SSL/CDN |
| 9. Documentation, grant reporting, demo materials | 8,000 | technical documentation, demo walkthroughs, architecture diagrams, reporting artifacts |
| 10. Contingency reserve | 12,000 | provider price changes, blocked sources, data reprocessing, storage/API overage |
| **Total** | **2,00,000** | 90-day functional MVP grant allocation |

## Lean Real Cash Cost vs Grant-Safe Budget

| Scenario | 90-Day Cost | Notes |
|---|---:|---|
| Barebones founder-built prototype | 65,000-95,000 | mostly free data, single VPS, minimal paid APIs, no paid data reserve |
| Functional MVP with 10-15 agents | 1,35,000-1,75,000 | enough API/cloud/data buffer to test real workflows |
| Grant-safe MVP ask | 2,00,000 | includes contingency, paid data reserve, evaluation reserve, reporting/demo polish |
| Hired-engineering commercial MVP | 8,00,000-20,00,000+ | if paying backend/AI/data/frontend engineers at market rates |

For a 2 lakh grant, the honest story is:

> The grant does not fully fund a commercial-grade product. It funds a credible, working MVP because founder/developer effort is contributed in-kind, and the grant is used for data, infrastructure, AI credits, validation, and demo readiness.

## Detailed Line Items

### 1. Market Data And Evidence Acquisition Reserve - INR 45,000

| Item | Estimate | Notes |
|---|---:|---|
| NSE/BSE historical and EOD data handling | 10,000 | scripts, storage, cleaning, corporate-action adjustment, error checks |
| Paid market-data/API trial reserve | 20,000 | placeholder until vendor quote; can cover one limited subscription or trial |
| Filing/tender/policy source monitoring | 5,000 | source snapshots, PDF/HTML storage, parser retries |
| Data quality correction reserve | 5,000 | symbol mapping, duplicates, bad rows, missing fields |
| Backup data procurement buffer | 5,000 | contingency for gaps in free/public sources |

Why this is defensible:

- NSE has official EOD/historical data subscription pages for exchange data.
- BSE publishes information-product pricing sheets.
- Free/public sources are useful but fragile; a grant budget should include a paid-data fallback.

### 2. AI Model/API Credits - INR 35,000

Estimated 90-day token budget for MVP:

| Workload | Approx Tokens |
|---|---:|
| ingestion classification and extraction | 80M-120M input, 10M-20M output |
| source summarization and evidence packs | 60M-100M input, 10M-20M output |
| research jobs and debate | 40M-80M input, 10M-20M output |
| synthesis and risk review | 20M-40M input, 5M-10M output |
| **Total MVP range** | **200M-340M input, 35M-70M output** |

Cost estimate:

| Provider Style | Approx 90-Day Cost |
|---|---:|
| DeepSeek-heavy routing | 10,000-30,000 |
| Qwen-heavy routing | 15,000-35,000 |
| OpenAI/Gemini mixed fallback | 25,000-60,000 |

Grant allocation: INR 35,000.

This assumes:

- cheap extraction models for routine parsing
- stronger reasoning models only for high-value synthesis
- prompt caching where available
- batch jobs for non-urgent tasks
- compact context packs instead of dumping full documents into prompts

### 3. Cloud Compute And Workers - INR 28,000

| Item | Estimate | Notes |
|---|---:|---|
| VPS / app server | 8,000-12,000 | API, scheduler, source polling, parsing jobs |
| worker capacity / second instance | 6,000-9,000 | background jobs, queue processing, replay jobs |
| bandwidth and snapshot overhead | 3,000-5,000 | backups, logs, file transfer |
| deployment/dev environments | 3,000-5,000 | staging and demo environment |
| buffer | 4,000 | short-term scaling during backfill |

Grant allocation: INR 28,000.

### 4. Database, Vector, Graph, Storage - INR 22,000

| Item | Estimate | Notes |
|---|---:|---|
| Postgres / Supabase Pro / managed DB | 7,000-10,000 | Supabase Pro is $25/month before overages |
| Object storage for raw evidence | 3,000-5,000 | PDFs, HTML snapshots, CSVs, reports |
| Vector store / pgvector | 3,000-5,000 | can start inside Postgres |
| Graph DB trial / self-hosted graph | 2,000-5,000 | Neo4j community, Memgraph, or Postgres graph tables |
| backups and retention | 3,000-5,000 | raw evidence must be replayable |

Grant allocation: INR 22,000.

### 5. Search / News / Research Tooling - INR 14,000

| Item | Estimate | Notes |
|---|---:|---|
| Search API / SERP credits | 5,000-8,000 | fallback for DuckDuckGo/search scraping fragility |
| RSS/source monitoring tools | 1,000-2,000 | official feeds and watchlists |
| crawler/proxy reserve | 3,000-5,000 | blocked pages, retries, rate limits |
| archive snapshots | 2,000 | store exact search/source evidence |

Grant allocation: INR 14,000.

### 6. Backtesting And Evaluation - INR 16,000

| Item | Estimate | Notes |
|---|---:|---|
| historical replay jobs | 4,000-6,000 | compute and storage for event windows |
| evaluation datasets | 3,000-5,000 | curated cases, false positives, missed catalysts |
| benchmark reporting | 2,000-3,000 | hit rate, lead time, false positives |
| QA reserve | 4,000 | test runs and reprocessing |

Grant allocation: INR 16,000.

### 7. Observability, Security, Backups - INR 12,000

| Item | Estimate | Notes |
|---|---:|---|
| logs / error tracking | 2,000-4,000 | can start free, budget for overages |
| uptime monitoring | 1,000-2,000 | API/source monitors |
| encrypted backups | 3,000-4,000 | evidence and database snapshots |
| secrets/security setup | 2,000 | password manager, key rotation, audit notes |

Grant allocation: INR 12,000.

### 8. Frontend Hosting, Domain, Deployment - INR 8,000

| Item | Estimate | Notes |
|---|---:|---|
| Vercel / frontend hosting | 0-6,000 | Hobby can be free; Pro is $20/month if commercial/team features are needed |
| domain | 1,000-2,000 | one year domain |
| demo deployment buffer | 1,000-2,000 | previews, DNS, SSL, CDN overage |

Grant allocation: INR 8,000.

### 9. Documentation, Grant Reporting, Demo Materials - INR 8,000

| Item | Estimate | Notes |
|---|---:|---|
| technical docs | 2,000 | architecture and data documentation |
| grant progress report | 2,000 | milestones, spend evidence, demo notes |
| demo screenshots/video | 2,000 | investor/grant committee review |
| polish reserve | 2,000 | final review and packaging |

Grant allocation: INR 8,000.

### 10. Contingency - INR 12,000

Used only for:

- API price changes
- source blocking or schema changes
- extra reprocessing
- unexpected storage growth
- temporary model escalation
- paid data sample requirement

## What The 2 Lakh Grant Should Not Promise

Do not promise:

- real-time exchange-grade live feed
- broker-grade intraday/tick data
- automated trading
- commercial data redistribution
- perfect small/mid-cap coverage from day one
- guaranteed alpha
- paid Bloomberg/Refinitiv-like data coverage

Promise instead:

- evidence-first MVP
- historical replay
- official/free/public source ingestion
- paid-data reserve
- 10-15 routed agents
- situation briefs with evidence IDs
- first backtesting loop
- terminal prototype

## Milestone-Based Spend Plan

### Month 1 - Evidence And Market Data Spine

Budget: INR 55,000

Deliverables:

- instrument universe
- raw evidence store
- NSE/BSE EOD ingestion
- filing/event ingestion
- Postgres schema
- source-health worker
- first parser agent

### Month 2 - Swarm And Situation Engines

Budget: INR 75,000

Deliverables:

- 10-15 agent registry
- model provider interface
- entity resolver
- search investigator
- graph writer
- price/volume features
- situation V1: order wins, results, unexplained price action, policy/tender tailwind

### Month 3 - Terminal, Backtesting, Demo

Budget: INR 70,000

Deliverables:

- terminal UI
- situation monitor
- evidence explorer
- agent trace panel
- research-job workflow
- event-study replay
- false-positive labels
- grant demo package

## Grant Narrative

Short version:

> HIVEMIND requires a 2 lakh MVP grant to build the evidence-first data foundation, agent orchestration layer, and prototype terminal for Indian capital-market intelligence. The funds will primarily cover data access, cloud infrastructure, AI/API credits, storage, validation, and demo readiness. Founder engineering work is contributed in-kind, which makes a functional MVP possible within the grant amount.

Long version:

> The MVP will not be a generic stock screener. It will demonstrate a repeatable architecture for capital-market situations: raw evidence ingestion, parsed records, feature generation, graph memory, model-agnostic AI agents, risk review, synthesis, and historical replay. The first system will use 10-15 routed agents and focus on end-of-day/historical intelligence rather than high-frequency trading. This lets the project cover small and mid-cap opportunities, policy and tender tailwinds, price-action anomalies, cross-asset shocks, and valuation context while keeping infrastructure costs controlled.

## Sources Checked

- DigitalOcean Droplet pricing: https://www.digitalocean.com/pricing/droplets
- Supabase pricing: https://supabase.com/pricing
- Vercel pricing: https://vercel.com/pricing
- DeepSeek API pricing: https://api-docs.deepseek.com/quick_start/pricing-details-usd/
- Alibaba Cloud / Qwen pricing: https://www.alibabacloud.com/help/en/model-studio/model-pricing
- OpenAI GPT-4.1 mini pricing: https://developers.openai.com/api/docs/models/gpt-4.1-mini
- NSE EOD/historical data subscription page: https://www.nseindia.com/static/market-data/eod-historical-data-subscription
- BSE Information Products pricing sheet: https://www.bseindia.com/downloads1/Information_Products_Pricing_Sheet.pdf
- USD/INR reference checked on 2026-06-09: https://currencylive.com/currency-converter/
