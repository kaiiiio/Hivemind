# HIVEMIND Data Foundation

Status: canonical data architecture and source plan  
Mode: free-first, paid-when-it-improves coverage/reliability  
Latency target: swing-trading best effort, not millisecond execution  
Coverage priority: full capital-markets foundation; equities/shares, debt/rates, commodities, FX, and derivatives context are all first-class

## 1. Purpose

The data foundation is HIVEMIND's market memory.

It answers:

- what happened
- where it came from
- when it was published
- when we fetched it
- which issuer, security, sector, commodity, currency, rate, derivative, policy, tender, or market event it affects
- whether price/volume/valuation confirmed it
- whether AI can reason over it safely

AI can improve ingestion, but AI cannot replace the source of truth. Raw evidence must exist before agents reason.

## 2. Source Strategy

Use three data tiers together:

| Tier | Role | Examples |
|---|---|---|
| Official truth | highest-trust evidence and replay | NSE, BSE, MCX, SEBI, RBI, MoSPI, PIB, CCIL, company filings |
| Paid speed/coverage | stable real-time or broader market-data access | TrueData, Global Datafeeds, Accelpix, Accord, broker APIs |
| Discovery/audit | find missed context and long-tail news | search engines, curated RSS, trade media, company sites, GitHub packages |

The system should never depend on only one tier.

## 3. Historical Data Backbone

Historical data is mandatory. It is not a later add-on and it is not the same problem as live market data.

HIVEMIND needs historical data for:

- event-study validation
- replaying what the system would have known at a past timestamp
- training situation thresholds
- detecting false positives and missed catalysts
- sector-relative and market-relative returns
- valuation history and "priced in" checks
- macro shock transmission analysis
- hedge and risk-offset analysis across futures/options where available
- source reconciliation and data-quality audits

Required historical datasets:

| Historical Dataset | Minimum Need | Why It Matters |
|---|---|---|
| daily OHLCV and delivery | all NSE/BSE equities, adjusted for corporate actions where possible | base replay, swing windows, liquidity, delivery confirmation |
| intraday candles | 1-minute or 5-minute where affordable; 5 years is useful | event timestamp reaction, gap/follow-through quality, liquidity |
| tick/depth history | optional for later; not needed for swing MVP | microstructure, slippage, order-flow research |
| corporate announcements and filings | raw PDFs/HTML plus parsed fields | event chronology and source-of-truth replay |
| corporate actions | splits, bonuses, dividends, symbol changes, mergers | adjusted price history and identity continuity |
| fundamentals and valuations | market cap, ratios, results, margins, debt, order book where available | "priced in" checks and business-quality context |
| macro/commodity/rates history | RBI, MoSPI, CCIL, MCX/global crude/metals/FX/yields | macro shock and sector exposure replay |
| derivatives and hedge context | F&O status, futures basis, options context, margin/risk where available | hedge feasibility and risk-offset replay |
| index/flow history | MSCI/FTSE/Nifty/BSE changes, F&O status, ASM/GSM, block/bulk | market-structure flow event studies |

The storage rule:

```text
historical raw/backfill -> normalized point-in-time features -> event windows -> outcome labels
```

Do not only store the latest value. For every feature used in a situation brief, store the value as of the event timestamp.

## 4. Recommended Market-Data Plan

### Best Price-To-Result Recommendation

Start with official/free sources plus one broker or vendor feed, then upgrade to an authorized market-data vendor when coverage and reliability become the bottleneck.

| Stage | Choice | Why |
|---|---|---|
| Local prototype | NSE/BSE bhavcopy and historical public downloads, BSE/NSE announcements, SEBI/RBI/MoSPI/PIB, CCIL, public commodity/FX/yield sources, derivative eligibility lists | Free, auditable, enough for EOD/swing discovery and first historical replay. |
| MVP historical + live beta | DhanHQ, Zerodha, FYERS, Breeze, Upstox, Angel SmartAPI as historical/live auxiliary APIs plus official EOD reconciliation | Confirmed public prices: DhanHQ Data API is listed at Rs 499 + taxes/month and includes daily/intraday historical APIs; Zerodha Connect is listed at Rs 500/month with historical candle data. FYERS, Breeze, Upstox, and Angel SmartAPI currently show free API access, subject to account eligibility and limits. |
| Serious beta | Accelpix and TrueData/Global Datafeeds pilots | Confirmed public benchmarks: Accelpix plans are listed at Rs 1,355 to Rs 2,965/month + GST and include EOD/intraday/tick history by plan; TrueData Velocity is listed at Rs 1,439.83 to Rs 2,795.83/month per segment. TrueData Market Data API and Global Datafeeds raw/API terms should be quoted directly for live + historical coverage. |
| Enterprise/product distribution | Direct exchange/vendor contracts and legal review | NSE domestic pricing effective April 1, 2026 lists examples such as CM EOD at Rs 1,00,000/year, CM historical trade data at Rs 1,10,000/year, and CM L1 internal display at Rs 24,40,000/year. BSE/MCX and redistribution rights are separate. |

Practical answer: for a founder beta, use free official sources plus Dhan/Zerodha/FYERS/Angel/ICICI only as auxiliary feeds. For "I need all capital-market data across shares, debt, commodities, FX and derivatives," budget for authorized vendors and exchange licensing after proof of concept. Broker APIs are cheap but account-tied and not a durable institutional market-data layer.

### Vendor Notes

| Provider | What The Source Says | Use In HIVEMIND | Caveat |
|---|---|---|---|
| TrueData | Market Data API page says authorized access to NSE, BSE, and MCX; pricing depends on exchange, symbols, and data type; exchange fees may be separate. Public Velocity pricing lists Rs 1,439.83 to Rs 2,795.83/month per segment. | Strong candidate for serious beta market feed. | Get direct quote for Market Data API subscription and license terms. Do not present Velocity pricing as final API pricing. |
| Global Datafeeds | Site says authorized realtime L1 vendor of NSE, MCX, BSE, NCDEX, and fundamental data. | Strong candidate where broad authorized coverage matters. | Pricing/API details require direct sales quote. |
| Accelpix | Public pricing lists Smart Rs 1,355/month, Pro Rs 2,118/month, and Ultimate Rs 2,965/month + GST, with symbol-at-a-time limits and current-day tick/1-minute/EOD history differences. API page says data is licensed for subscriber charting/analysis. | Good price-to-result for personal/research/charting workflows. | Verify limits, symbols-at-a-time, redistribution, and API terms. |
| DhanHQ | Support page lists Data API subscription at Rs 499 + taxes/month for live feed, quotes, historical, intraday. Docs say daily historical data is available back to stock inception and intraday historical data is available for the last 5 years in 1/5/15/25/60 minute intervals, with 90-day request windows. | Cheap MVP live + historical data lane. | Broker account dependency, rate limits, and quality checks required. |
| Zerodha Kite Connect | Support page lists Connect at Rs 500/month with real-time WebSockets and historical candles; Personal plan has no historical/real-time data. Docs describe archived candle data across exchanges in minute/3-minute/5-minute/hourly/daily intervals. | Cheap, well-documented MVP live + historical auxiliary lane. | Broker account dependency and app/user constraints. |
| FYERS / ICICI Breeze / Upstox / Angel SmartAPI | Official pages describe free APIs with market-data and historical-data capabilities. Breeze states historical data/API access is free for ICICIdirect customers; Angel SmartAPI FAQ states historical data is free and available for all segments. | Useful auxiliary historical/live feeds and cross-checks. | Quality, rate limits, authentication, static-IP requirements, and historical depth must be tested. |
## 5. Source Matrix

| Source Class | Sources | What To Store | Cadence |
|---|---|---|---|
| Equity official events | BSE announcements/RSS, NSE announcements/RSS, company filings | announcements, PDFs, XBRL, timestamps, categories, raw text | hot: 15-60 sec best effort where permitted |
| Equity EOD | NSE/BSE bhavcopy, all reports, delivery, corporate actions | OHLCV, turnover, delivery, series/group, corporate actions | EOD |
| Security master | NSE/BSE listed security files, ISIN mapping | instrument universe, aliases, BSE code, NSE symbol, SME flag, status | daily + weekly diff |
| Commodities/metals | MCX official datafeed/bhavcopy, paid vendor, global metals references | futures/spot where available, crude/gas/metals moves | EOD first; faster later |
| Bonds/rates | RBI DBIE, CCIL bond/money-market data, G-sec yields | rates, yields, liquidity, bond-market indicators | daily/monthly by source |
| Derivatives/hedging | NSE/BSE F&O lists, futures/options snapshots from broker/vendor where permitted | F&O eligibility, futures basis, options context, hedge availability | EOD first; faster later |
| Macro | RBI DBIE, MoSPI/eSankhyiki, CPI/WPI/IIP/GDP, FRED/World Bank where relevant | macro indicators and release timestamps | release-driven |
| Policy/regulatory | PIB RSS, SEBI RSS, RBI, ministries, cabinet releases | policy events, schemes, circulars, enforcement, sector tags | 1-60 min |
| Tenders/procurement | CPPP, GeM, IREPS, PSU portals, sector portals | tender title, buyer, amount, dates, eligibility, L1/award | daily first |
| Market structure | MSCI, FTSE Russell, NSE/BSE index notices, AMFI classification, F&O lists, ASM/GSM, block/bulk | inclusion/exclusion, weight changes, effective dates, flow estimates | event-driven |
| Search/news | DuckDuckGo/search APIs, RSS, trade media, company IR | result metadata, snippets, article text, source quality | triggered |

## 6. Ingestion Swarm

Data ingestion needs its own swarm because the hard problem is not just fetching. It is cleaning, resolving, reconciling, and not missing edge cases.

### First 10-15 Workers/Agents

| Agent / Worker | Job |
|---|---|
| Scheduler Worker | runs source-specific polling jobs with backoff and market-calendar awareness |
| Source Health Agent | detects source downtime, schema drift, Cloudflare/blocking, timestamp anomalies |
| Raw Evidence Worker | stores every fetched payload with checksum before parsing |
| PDF/XBRL Parser Agent | extracts text, tables, values, and filing sections |
| CSV/API Normalizer Worker | normalizes bhavcopy, delivery, index, and vendor payloads |
| Entity Resolver Agent | maps company names, aliases, symbols, BSE codes, ISINs, customers, ministries |
| Event Classifier Agent | classifies order wins, results, capex, rating, governance, policy, tender, flow events |
| Materiality Agent | computes order size vs market cap/revenue/order book, event severity, liquidity impact |
| Cross-Asset Mapper Agent | maps crude, metals, FX, rates, geopolitical risk, and freight to sector/company exposure |
| Tender Mapper Agent | maps tender categories to likely listed beneficiaries |
| Search Auditor Agent | runs targeted missed-event and unexplained-move investigations |
| Graph Writer Agent | writes company-sector-policy-tender-customer-event relationships |
| Dedupe/Synthesis Worker | merges duplicate filings/articles/vendor records into canonical events |
| Quality Gate Agent | rejects unsupported AI claims and marks DATA_GAP when evidence is weak |
| Feature Writer Worker | writes price, valuation, flow, macro, and situation feature snapshots |

## 7. Processing Policy

Do not process every source with the same intensity.

| Stage | Run For | Cost |
|---|---|---|
| deterministic fetch and raw storage | full universe | low |
| rules/parsers/features | full universe | low/medium |
| cheap AI extraction | new filings, PDFs, tenders, unclear categories | medium |
| search investigation | only triggered candidates and audit lists | medium |
| multi-agent research | only active situation candidates | high |
| strongest model final brief | only user-facing/high-priority situations | highest |

This is how broad coverage stays affordable.

## 8. Data Freshness Tiers

| Tier | Target | Sources | Use |
|---|---|---|---|
| Hot | 15-60 sec best effort | BSE/NSE announcements, selected RSS, paid feed if available | material corporate events |
| Warm | 1-10 min | SEBI, PIB, company sites, curated news, vendor snapshots | regulatory/policy/context updates |
| Batch | EOD | bhavcopy, delivery, valuation snapshots, CCIL/RBI/MoSPI updates | daily situation scoring and replay |
| Audit | daily/weekly | search, GitHub/open-source checks, source diffs | missed-event detection |

## 9. Storage Model

Minimum tables:

| Table | Purpose |
|---|---|
| instruments | one row per tradable/listed instrument with ISIN, NSE symbol, BSE code, aliases, sector, cap bucket, SME flag |
| source_registry | source URL/API, trust level, cadence, owner, ToS notes |
| raw_evidence | immutable source payloads with URL, timestamps, checksum, raw path/text |
| parsed_documents | extracted text, tables, parser version, parse quality |
| entity_links | document/company/security/customer/ministry/sector links |
| parsed_events | event candidates extracted from evidence |
| canonical_events | deduped decision-grade events |
| price_daily | OHLCV, turnover, value traded |
| delivery_daily | delivery quantity and percentage |
| valuation_snapshots | market cap, multiples, growth/margins/debt/order book |
| market_structure_events | MSCI/FTSE/Nifty/BSE/F&O/surveillance/block/bulk events |
| macro_shock_events | crude, metals, FX, rates, geopolitical, freight, and global-risk events |
| tailwind_events | policy, budget, regulator, sector, tender tailwinds |
| situations | situation candidates with evidence IDs and feature snapshots |
| model_runs | provider/model/prompt/evidence/output/cost audit |
| source_health | latency, failures, schema drift, blocked flags |
| ingestion_audit | run-level counts, misses, failures, freshness |

Storage policy:

- raw evidence is the canonical archive
- parsed tables and facts go to relational/columnar stores
- market data and derived features go to time-series/feature tables
- embeddings go to vector stores only for searchable chunks and similarity retrieval
- relationships go to graph tables or a graph database
- agent outputs, prompt versions, context packs, and costs go to model-run tables
- outcomes and post-mortems go to outcome memory
- every vector chunk and graph edge must link back to raw evidence or a versioned derived record

## 10. Event Taxonomy V1

Corporate:

- order_win
- contract_extension
- tender_win
- result_growth
- margin_expansion
- capex
- debt_reduction
- fundraise
- promoter_buying
- promoter_pledge_change
- rating_upgrade
- merger_acquisition
- regulatory_approval
- litigation_risk
- governance_risk

Market behavior:

- volume_expansion
- delivery_spike
- breakout
- failed_breakout
- relative_strength
- unexplained_gap
- multi_day_accumulation
- liquidity_discovery

Market structure:

- MSCI_inclusion
- MSCI_exclusion
- FTSE_inclusion
- FTSE_exclusion
- Nifty_index_inclusion
- Nifty_index_exclusion
- BSE_index_inclusion
- BSE_index_exclusion
- FNO_inclusion
- FNO_exclusion
- ASM_GSM_surveillance
- bulk_deal
- block_deal
- passive_flow_rebalance

Macro shock:

- crude_oil_shock
- natural_gas_shock
- metal_price_shock
- USDINR_shock
- bond_yield_shock
- geopolitical_escalation
- sanctions
- shipping_disruption
- global_risk_off
- import_export_policy_change
- supply_chain_disruption

Policy/tender:

- rate_cut
- rate_hike
- liquidity_easing
- budget_allocation
- PLI_scheme
- import_duty_change
- export_incentive
- defence_procurement
- railway_capex
- renewable_policy
- data_center_policy
- new_tender
- tender_corrigendum
- L1_result
- tender_award

## 11. Search Engine Use

Search engines should be used aggressively but intelligently.

Bad:

```text
Search the whole web for all market news.
```

Good:

```text
Unexplained price action detected.
Generate targeted queries using company aliases, sector, suspected event, date range, tenders, and filings.
Store result metadata.
Classify source quality.
Verify against official sources where possible.
Attach evidence to the situation.
```

Search outputs candidate evidence, not truth.

Source quality:

| Level | Source | Use |
|---|---|---|
| A | exchange, regulator, government, company | truth |
| B | rating agencies, reputed financial media | strong context |
| C | trade/local/sector publications | discovery |
| D | social/forums/SEO aggregators | weak clue only |

## 12. AI-Assisted Research And Knowledge Intake

Data ingestion should not be manual. AI should help discover sources, parse documents, reconcile entities, and audit misses, while deterministic storage preserves raw evidence.

### Research Prompt Intake

Complex prompts should be stored as `research_jobs`, not handled as disposable chat.

Example job classes:

| Job Class | Example | Data Foundation Work |
|---|---|---|
| forensic equity screen | broker target upside plus ROCE/CFO/debt/pledge/growth filters | broker PDF archive, earnings tables, shareholding data, valuation snapshots |
| unexplained price-action audit | price run without visible official news | price window, search results, exchange filings, sector/news audit |
| policy/tender beneficiary map | new scheme, tender wave, budget allocation | tender records, ministry/PSU buyer graph, listed supplier links |
| macro shock study | crude, metals, FX, rates, geopolitical shock | commodity/FX/rate time series, sector exposure graph, margin sensitivity |
| market-structure event | MSCI/FTSE/index/F&O inclusion | index notices, effective dates, flow estimates, liquidity history |

Each research job writes:

- job spec and prompt
- source plan
- raw evidence IDs
- extracted facts
- accepted candidates
- rejected candidates and reasons
- agent outputs and debate summaries
- final report
- later outcome labels

### Knowledge Artifact Types

| Artifact | Truth Status | Use |
|---|---|---|
| official filing/source record | verified evidence | can support facts |
| broker report | institutional evidence | can support target, estimates, and thesis with date/source |
| news/trade article | contextual evidence | discovery and triangulation |
| user observation | hypothesis | trigger search, never treated as verified fact |
| AI-generated note | derived artifact | routing/search aid, not source of truth |
| post-mortem | outcome evidence | improves thresholds, prompts, routing, and guardrails |

### AI Ingestion Rules

- AI may generate search queries, source lists, parser hints, entity candidates, and missing-evidence audits.
- AI may extract facts from documents only when it returns spans, tables, page numbers, source URLs, timestamps, and confidence.
- AI may propose new source adapters, but adapters must still store raw payloads and pass reconciliation tests.
- AI may summarize knowledge artifacts, but summaries must never replace raw evidence.
- AI may update agent lessons from post-mortems, but prompt and routing changes must be versioned.

## 13. GitHub And Package Policy

Useful packages can accelerate early work but must be wrapped behind HIVEMIND adapters.

| Package/Repo | Use | Policy |
|---|---|---|
| jugaad-data | NSE/bhavcopy helpers | verify output against official records |
| nsepython / NseIndiaApi | public NSE endpoint helpers | use for learning/endpoints, not as sole truth |
| BseIndiaApi / bseindia | BSE public data helpers | verify and store raw URLs |
| yfinance | broad global fallback | useful for global context, not official Indian data |
| broker SDKs | live quotes/websocket and historical candles | reconcile with official EOD |

Rules:

- store package name/version in ingestion audit
- keep our own source adapters
- raw official evidence wins over package output
- test packages for silent schema changes
- never rely on undocumented scraping for investor-grade claims without reconciliation

## 14. Sprint 1 Scope

Mandatory:

1. instrument master
2. raw evidence store
3. adapter interface
4. BSE/NSE announcement ingestion
5. EOD price/volume ingestion
6. basic event parser for order wins, results, capex, ratings, promoter activity
7. source health table
8. material order-win situation replay

Optional:

- SME board coverage
- paid broker feed adapter
- tender discovery
- search audit
- AI extraction fallback

Out of scope:

- execution/trading automation
- millisecond tick processing
- redistributing paid market data
- recommendation automation without evidence and risk controls

## 15. First Implementation Files

```text
hivemind/data_foundation/models.py
hivemind/data_foundation/storage/sqlite_store.py
hivemind/data_foundation/adapters/base.py
hivemind/data_foundation/adapters/bse/announcements.py
hivemind/data_foundation/adapters/nse/announcements.py
hivemind/data_foundation/adapters/marketdata/broker_feed.py
hivemind/data_foundation/parsing/events.py
hivemind/data_foundation/scoring/swing_score.py
hivemind/data_foundation/cli/run_once.py
```

Use SQLite first for speed. Move to PostgreSQL/TimescaleDB after schemas and adapters stabilize.

## 16. Reference Links

- NSE real-time data subscription: https://www.nseindia.com/market-data/real-time-data-subscription
- NSE RSS: https://www.nseindia.com/rss-feed
- BSE market data products: https://www.bseindia.com/market_data_products.html?flag=real
- BSE RSS feeds: https://www.bseindia.com/rss-feed.html
- MCX datafeed: https://www.mcxindia.com/technology/datafeed
- CCIL bond market data: https://www.ccilindia.com/web/ccil/bond-market
- SEBI RSS: https://www.sebi.gov.in/rss.html
- RBI DBIE: https://data.rbi.org.in/DBIE/
- MoSPI eSankhyiki Python library: https://www.mospi.gov.in/esankhyiki-python-library
- PIB RSS: https://www.pib.gov.in/ViewRss.aspx?lang=1&reg=20
- TrueData Market Data API: https://www.truedata.in/market-data-apis
- TrueData pricing: https://www.truedata.in/information/pricing
- Global Datafeeds: https://globaldatafeeds.in/
- Accelpix pricing: https://accelpix.com/pricing/
- Accelpix APIs: https://accelpix.com/pix-apis/
- DhanHQ data API support: https://dhan.co/support/platforms/dhanhq-api/how-can-i-access-live-market-data-through-dhan/
- DhanHQ historical data docs: https://dhanhq.co/docs/v2/historical-data/
- Zerodha Kite API charges: https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/what-are-the-charges-for-kite-apis
- Zerodha historical candle docs: https://kite.trade/docs/connect/v3/historical/
- FYERS API: https://fyers.in/products/api/
- Angel SmartAPI FAQ: https://smartapi.angelbroking.com/faq
- ICICI Breeze API: https://www.icicidirect.com/futures-and-options/api/breeze
- NSE domestic market data pricing: https://nsearchives.nseindia.com/web/mediaattachment/2026-04/Download_Pricing_file_-_Domestic_clients_20260424122229.pdf
