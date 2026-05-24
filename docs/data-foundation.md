# HIVEMIND Data Foundation

Status: Canonical implementation and source plan  
Mode: Free-first, best-effort, swing-trading latency  
Coverage priority: small caps and mid caps first, large caps second, SME optional  

## 1. Purpose

The data foundation is the market memory of HIVEMIND.

It answers:

- what happened
- where it came from
- when it was published
- when we fetched it
- which company or sector it affects
- whether the market confirmed it
- whether AI can reason over it safely

The data foundation must exist before the AI swarm. Without it, agents become summarizers of whatever happens to be found. With it, every agent receives auditable evidence, timestamps, source freshness, and context.

## 2. Executive Decision

Do not rely on AI or search engines as the primary source of market data.

Use official exchange, regulator, government, company, and reproducible public sources as the source of truth.

Use AI only after raw evidence is stored.

Use search engines only for triggered investigation, source discovery, and missed-event audit.

## 3. Coverage Goal

The ingestion layer must not filter out companies because they are small, illiquid, outside major indices, or poorly covered by media.

Mandatory:

- NSE mainboard
- BSE mainboard
- BSE-exclusive equities
- small-cap and mid-cap coverage
- ISIN-first identity mapping where possible
- NSE symbol, BSE scrip code, company aliases, and old names

Optional but supported:

- NSE SME
- BSE SME

Small and mid caps are mandatory because one contract, pledge release, rating upgrade, tender win, or policy tailwind can re-rate the stock faster than in large caps.

## 4. Source Priority Model

| Priority | Source Type | Role | Trust Level |
|---|---|---|---|
| P0 | NSE/BSE filings and announcements | Corporate events, results, order wins, disclosures | Highest |
| P0 | NSE/BSE bhavcopy and reports | EOD price, volume, delivery, corporate actions | Highest |
| P0 | Security master files | Tradable universe and identifiers | Highest |
| P1 | SEBI/RBI/MoSPI/PIB releases | Regulation, macro, policy tailwinds | High |
| P1 | Government procurement portals | Tender and order pipeline clues | High but fragmented |
| P2 | Company investor relations pages | Press releases, presentations, annual reports | High |
| P2 | Reputed news and sector publications | Context, discovery, narrative confirmation | Medium |
| P3 | GitHub packages and unofficial APIs | Engineering acceleration | Verify against official data |
| P3 | Search engines | Missed-event audit and source discovery | Fallback only |

## 5. Source Matrix

| Source Class | Public Source | What To Ingest | Cadence | Priority |
|---|---|---|---|---|
| Exchange EOD | NSE all reports, BSE bhavcopy | OHLCV, turnover, delivery, corporate actions | EOD | P0 |
| Security master | NSE/BSE listed security files | symbol, ISIN, series/group, active status, SME flag | daily + weekly diff | P0 |
| Corporate announcements | NSE/BSE announcements and RSS | raw announcement, PDF/XBRL, title, timestamp, ticker | 15-60 sec best effort where allowed | P0 |
| Regulator | SEBI RSS/orders/circulars | circulars, enforcement, orders, market rules | 1-5 min | P1 |
| Macro | RBI, MoSPI/eSankhyiki | rates, liquidity, inflation, IIP, GDP, sector indicators | daily/weekly/monthly | P1 |
| Policy | PIB, ministries, cabinet releases | schemes, capex, procurement, sector policy | 5-60 min by source | P1 |
| Tenders | CPPP/eProcure, GeM, IREPS, PSU portals | new tenders, awards, L1, procurement plans | daily first, faster later | P1/P2 |
| Company websites | IR pages and press releases | press releases, order details, presentations | candidate-triggered + daily | P2 |
| News/RSS | financial and sector media | headline, URL, timestamp, mentioned entities | source dependent | P2 |
| Search engine | DuckDuckGo/other search | missed-event check, source discovery | triggered + daily audit | P3 |

## 6. Useful GitHub Repos And Packages

These tools can accelerate development, but should be wrapped behind our own adapter interfaces.

| Tool | Language | Potential Use | Link |
|---|---|---|---|
| jugaad-data | Python | NSE historical/bhavcopy helpers | https://github.com/jugaad-py/jugaad-data |
| nse-bse-api | TypeScript | Unified NSE/BSE wrappers | https://github.com/bshada/nse-bse-api |
| BseIndiaApi | Python | BSE announcements/actions helper | https://github.com/BennyThadikaran/BseIndiaApi |
| NseIndiaApi | Python | NSE unofficial API helper | https://github.com/BennyThadikaran/NseIndiaApi |
| Indian-Stock-Market-API | Python/Flask | Yahoo-backed NSE/BSE quote API | https://github.com/0xramm/Indian-Stock-Market-API |
| bhavCopy-downloader | JavaScript/Go | NSE/BSE bhavcopy downloader | https://github.com/girishg4t/bhavCopy-downloader |
| stocky | Python | ISIN/symbol mapping | https://github.com/rehanhaider/stocky |
| bseindia | Python | BSE public data wrapper | https://pypi.org/project/bseindia/ |

Package policy:

- prefer official-source adapters for core ingestion
- use packages to learn endpoints and speed early development
- compare package output against raw official records
- store source name, package version, fetch timestamp, and URL
- never let a package become the only evidence source for material events

## 7. Processing Lanes

The data foundation should not be one giant scraper. It should be a set of lanes, each with its own trigger and evidence rules.

| Lane | Question | First Sources | Output |
|---|---|---|---|
| Official Events | Did the company disclose something material? | BSE/NSE/company filings | structured corporate event |
| Price/Volume | Is the market behaving like something changed? | bhavcopy, delivery, OHLCV | market behavior event |
| Macro/Policy | Did policy or macro improve a sector outlook? | RBI, SEBI, MoSPI, PIB, ministries | tailwind event |
| Tender/Procurement | Are future orders forming before company disclosure? | CPPP, GeM, IREPS, PSU portals | tender pipeline event |
| Search/News | Is there public context not captured elsewhere? | search, media, trade publications | candidate evidence |
| Fundamentals | Can the company benefit from the catalyst? | results, annual reports, presentations | business quality context |

## 8. Ingestion Pipeline

| Stage | Component | Behavior | Storage Output |
|---|---|---|---|
| 1 | Universe Builder | Builds full NSE/BSE universe, aliases, ISIN mapping, SME flag | instruments |
| 2 | Source Pollers | Fetches announcements, RSS, bhavcopy, circulars, tenders | raw_evidence candidates |
| 3 | Raw Evidence Store | Stores raw content, URL, timestamps, checksum | raw_evidence |
| 4 | Parser Layer | Extracts text/tables from HTML, CSV, PDF, XBRL | parsed_document |
| 5 | Entity Resolver | Maps names, symbols, scrip codes, ISINs | document_instrument_link |
| 6 | Event Extractor | Rules first, AI second; creates structured events | parsed_events |
| 7 | Dedupe + Fusion | Merges same event across exchange/company/news sources | canonical_events |
| 8 | Situation Engines | Creates material order-win, tailwind, tender, price-action situations | situations |
| 9 | Alert Scorer | Computes situation-specific attention priority | alerts |
| 10 | Memory Writers | Writes timeseries, vectors, graph relationships, hot state | AI layer inputs |

## 9. Storage Model

Minimum tables:

| Table | Purpose | Important Fields |
|---|---|---|
| instruments | one row per listed/tradable instrument | instrument_id, ISIN, NSE symbol, BSE code, name, sector, market cap bucket, SME flag |
| raw_evidence | immutable evidence before parsing | source, URL, fetched_at, published_at, checksum, raw_path, raw_text |
| parsed_document | extracted text/tables | evidence_id, parser_version, text, table_json, parse_quality |
| parsed_events | structured event candidates | event_type, instrument_id, amount, confidence, evidence_span |
| canonical_events | deduped event | event_id, primary_instrument_id, source_priority, severity, summary |
| price_daily | EOD price/volume | instrument_id, date, OHLCV, turnover |
| delivery_daily | delivery confirmation | instrument_id, date, delivery_qty, delivery_pct |
| tailwind_events | macro/policy/tender context | source, title, sectors_impacted, tags, time_horizon |
| situations | thesis candidates | situation_type, evidence_ids, company, materiality, uncertainty |
| alerts | final attention queue | situation_id, priority, reason, status |
| source_health | source monitoring | source_name, last_success_at, latency, error_rate, blocked_flag |
| ingestion_audit | run-level audit | run_id, source, records_seen, records_new, records_failed |

## 10. Event Taxonomy V1

Corporate events:

- order_win
- contract_extension
- tender_win
- result_growth
- margin_expansion
- capex
- debt_reduction
- fundraise
- promoter_buying
- insider_trade
- rating_upgrade
- merger_acquisition
- product_launch
- regulatory_approval
- litigation_risk
- pledge_change

Macro/policy events:

- rate_cut
- rate_hike
- liquidity_easing
- budget_allocation
- PLI_scheme
- import_duty_change
- export_incentive
- government_capex
- sector_policy_change
- defence_procurement
- railway_capex
- renewable_policy
- data_center_policy
- digital_infra_policy

Tender/procurement events:

- new_tender
- tender_corrigendum
- tender_award
- L1_result
- GeM_bid
- PSU_procurement_plan

Market behavior events:

- volume_expansion
- delivery_spike
- breakout
- relative_strength
- unexplained_gap
- multi_day_accumulation
- sector_rotation

## 11. Smart Search Engine Use

Search engines are not a live market data feed.

Use search when there is a reason to investigate:

- unexplained price action
- high-materiality official event
- policy tailwind with unclear beneficiaries
- tender category with possible listed beneficiaries
- company enters watchlist
- daily missed-event audit

Search workflow:

1. Generate targeted queries from company aliases, sector, event suspicion, and date range.
2. Fetch candidate results from available search sources.
3. Store search result metadata as evidence.
4. Classify source quality.
5. Extract candidate evidence.
6. Verify against official or high-trust sources when possible.
7. Attach findings to a situation.

Source quality:

| Level | Source | Use |
|---|---|---|
| A | exchange, regulator, government, company | truth source |
| B | reputed financial media, rating agency | strong context |
| C | sector, trade, local media | discovery |
| D | social, forums, SEO aggregators | weak clue only |

## 12. AI In The Data Foundation

AI can make ingestion smarter, but only after raw evidence is stored.

Use AI for:

- company/entity matching
- announcement classification
- PDF/text summarization
- amount/customer/timeline extraction
- sector/tailwind tagging
- tender-to-company matching
- duplicate clustering
- explanation generation

Do not use AI for:

- price data
- invented financial metrics
- unsupported event claims
- final alerts without evidence links

Every AI output must include:

- source evidence id
- extracted fields
- confidence
- uncertainty
- evidence quote/span

## 13. Scoring Philosophy

The system should not create one generic stock score first.

It should create situation-specific scores:

- order_win_score
- tailwind_score
- price_action_score
- tender_pipeline_score
- result_rerating_score
- theme_rotation_score

Then it should produce an attention priority from the strongest active situation.

Example factors:

| Factor | Meaning |
|---|---|
| source trust | exchange/regulator/company beats media/search |
| event materiality | order size vs market cap/revenue/order book |
| small/mid-cap relevance | higher sensitivity to catalyst size |
| tailwind match | sector/policy/tender alignment |
| market confirmation | price, volume, delivery, relative strength |
| recency | fresh evidence gets priority |
| novelty | duplicate and stale news is penalized |
| risk modifier | governance, pledge, litigation, execution risk |

## 14. Dynacons-Style Replay Test

Dynacons-style events should be regression tests.

Expected flow:

1. Fetch exchange/company announcement.
2. Store raw evidence before parsing.
3. Resolve company to NSE/BSE/ISIN identity.
4. Extract order value, counterparty, duration, and event type.
5. Compare order value to company scale.
6. Map sector and tailwind tags.
7. Check price/volume confirmation.
8. Emit a high-attention situation even if mainstream media has not covered it yet.

Expected situation:

```json
{
  "situation_type": "material_order_win_small_mid_cap",
  "event_type": "order_win",
  "event_amount_inr_cr": 750,
  "tailwinds": ["government_it_spend", "digital_infrastructure"],
  "evidence_strength": "official",
  "market_confirmation": "pending_or_present"
}
```

## 15. Latency Tiers

| Tier | Target | Sources | Use Case |
|---|---|---|---|
| Hot | 15-60 seconds best effort | BSE/NSE announcements where stable | material announcements |
| Warm | 1-10 minutes | SEBI RSS, company pages, curated RSS | regulatory and narrative context |
| Batch | EOD | bhavcopy, delivery, security master | backtesting and daily scoring |
| Audit | daily/weekly | search, media sweeps, source diffs | missed-event detection |

## 16. Free Infrastructure

| Function | Recommended Free Component |
|---|---|
| scheduler | APScheduler or cron first |
| HTTP ingestion | httpx or aiohttp with rate limits and backoff |
| RSS | feedparser |
| parsing | pandas, BeautifulSoup, lxml, pypdf/PyMuPDF |
| database | SQLite first, PostgreSQL/TimescaleDB later |
| hot state | Redis |
| vector store | Qdrant |
| graph | Neo4j Community |
| search index | PostgreSQL full text first |
| monitoring | source_health and ingestion_audit tables first |

## 17. Sprint 1 Scope

Mandatory:

- instrument master
- raw evidence store
- adapter interface
- BSE/NSE announcement ingestion
- EOD price/volume ingestion
- event parser for order wins, results, capex, ratings, promoter activity
- basic situation scoring
- Dynacons replay

Optional:

- SME coverage
- tender discovery
- search audit
- AI extraction fallback

Out of scope:

- paid feeds
- tick-level streaming
- millisecond latency
- execution/trading automation
- portfolio recommendation automation

## 18. First Implementation Files

Start with:

```text
hivemind/data_foundation/models.py
hivemind/data_foundation/storage/sqlite_store.py
hivemind/data_foundation/adapters/base.py
hivemind/data_foundation/adapters/bse/announcements.py
hivemind/data_foundation/adapters/nse/announcements.py
hivemind/data_foundation/parsing/events.py
hivemind/data_foundation/scoring/swing_score.py
hivemind/data_foundation/cli/run_once.py
```

Use SQLite first for speed. Move to PostgreSQL/TimescaleDB after source adapters and schemas stabilize.

## 19. Sprint 1 Milestones

| Milestone | Deliverable | Acceptance |
|---|---|---|
| Universe | instrument master, symbol mapping, cap bucket, SME flag | every event maps to an instrument or unresolved queue |
| Raw Evidence | raw_evidence table, content hash, adapter base | no fetched item is parsed before being stored |
| Announcements | BSE/NSE announcement adapters | order-win, results, corporate action, rating events detected |
| Price/Volume | bhavcopy ingestion and OHLCV table | alerts show 1-day, 3-day, 5-day context |
| Tailwinds | SEBI/RBI/MoSPI/PIB ingestion | policy events map to sectors and candidate companies |
| Dynacons Replay | historic replay script | material order-win situation is detected and explained |

## 20. Acceptance Criteria

- security master covers NSE mainboard, BSE mainboard, BSE-exclusive names, and optional SME boards
- EOD ingestion validates missing or malformed files
- announcements are stored as raw evidence before parsing or AI calls
- every AI-extracted event cites evidence id, source URL, timestamp, and confidence
- Dynacons-style order-win replay emits high attention without relying on media coverage
- daily audit compares exchange announcements, RSS/media, and search results for misses
- agents receive `DATA_GAP` when evidence freshness or quality is insufficient

## 21. Reference Links

- NSE all reports: https://www.nseindia.com/all-reports
- NSE corporate announcements: https://www.nseindia.com/companies-listing/corporate-filings-announcements
- NSE corporate data subscriptions: https://www.nseindia.com/market-data/corporate-data-subscription
- BSE bhavcopy: https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx
- BSE RSS feeds: https://www.bseindia.com/rss-feed.html
- SEBI RSS: https://www.sebi.gov.in/rss.html
- RBI DBIE: https://data.rbi.org.in/DBIE/
- eSankhyiki: https://www.esankhyiki.com/
- NIC eProcurement: https://www.nic.gov.in/project/government-e-procurement-system/

