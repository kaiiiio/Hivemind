# HIVEMIND AI Layer

Status: canonical model-agnostic AI-swarm design  
Audience: AI engineering, backend, quant, data engineering  
Goal: make AI the operating intelligence across ingestion, research, graph construction, quant validation, risk, and final synthesis

## 1. Core Rule

AI is not the market data source.

AI does the heavy lifting after evidence exists:

- parses messy documents
- resolves entities
- maps events to sectors and companies
- investigates missing context
- builds graph relationships
- compresses evidence into context packs
- runs specialist reasoning
- challenges unsupported claims
- produces final situation briefs

Every important AI output must cite evidence IDs.

## 2. Model-Agnostic Boundary

Agents must not depend on Gemini, GPT, DeepSeek, Qwen, Claude, Groq, local models, or any single provider.

All agents call a common provider interface:

```python
class AIModelProvider:
    name: str

    async def generate(self, request: AIRequest) -> AIResponse:
        ...

    async def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        ...
```

Provider adapters:

- `MockProvider` for local development and deterministic tests
- `DeepSeekProvider` for cheap long-context and reasoning calls
- `QwenProvider` for bulk classification/extraction
- `GeminiProvider` when Google API credits/keys are available
- `OpenAIProvider` when GPT models are needed
- `LocalProvider` for self-hosted open-weight models later

Agents receive a provider through dependency injection. They never import vendor SDKs directly.

## 3. Swarm Everywhere

The AI layer is not one endpoint called at the end. It is fused into every pipeline.

| Pipeline | AI Work |
|---|---|
| Ingestion | source monitoring, filing classification, parsing, entity resolution, schema drift explanation |
| Search | query generation, source quality scoring, duplicate clustering, official-source verification |
| Graph | entity/relationship extraction, alias merging, company-sector-policy-tender linkage |
| Situation engines | materiality explanation, missing-field detection, uncertainty tags |
| Quant validation | event-study interpretation, anomaly classification, false-positive review |
| Risk | valuation, liquidity, governance, execution, crowding, balance-sheet challenge |
| Synthesis | opportunity/risk review, uncertainty preservation, evidence-cited final brief |

### Why Swarms Are The Product Intelligence

HIVEMIND Terminal should sell swarm intelligence, not just AI summaries.

A single LLM can draft a report. A swarm can operate a market terminal:

| Single-Model Pattern | Swarm Intelligence Pattern |
|---|---|
| one large prompt tries to do everything | router selects the right agents for the situation |
| generic reasoning over mixed context | source, sector, quant, valuation, macro, and risk specialists |
| hard to know why the answer changed | each agent writes structured evidence, confidence, and uncertainty |
| expensive if every task uses a strong model | cheap agents handle extraction; strong models handle rare hard synthesis |
| narrative risk | risk-review agents force counter-evidence and missing-fact disclosure |

The terminal must expose this intelligence:

- show which agents ran
- show consensus and uncertainty
- show missing evidence
- show confidence by source quality, materiality, price confirmation, and valuation
- let the user launch targeted follow-up research from any terminal screen

This makes the pitch sharper:

```text
HIVEMIND is a swarm intelligence terminal, not a generic assistant wrapped around market data.
```

## 4. Agent Pools

### Core 10-15 Agent/Worker Set

| Agent | Output |
|---|---|
| Orchestrator/Router | selected agent plan, model budget, priority |
| Source Health Agent | source status, freshness, schema drift, failures |
| Evidence Intake Agent | source type, priority, required parser |
| Filing Parser Agent | extracted fields, spans, confidence |
| Entity Resolver Agent | instrument/company/customer/ministry mappings |
| Market Behavior Agent | price, volume, delivery, liquidity interpretation |
| Macro/Policy Agent | sector impact map and time horizon |
| Tender Agent | tender category, likely beneficiaries, uncertainty |
| Search Investigator Agent | query set, candidate evidence, verification status |
| Graph Builder Agent | nodes/edges to write |
| Valuation Agent | priced-in/euphoric/cheap context |
| Quant Validator Agent | event study, peer-relative and regime checks |
| Bull Case Agent | strongest evidence-backed upside thesis |
| Risk Review Agent | risks, unsupported claims, missing facts |
| Synthesis Agent | final situation brief |

### Agent Personality And Bias Model

Every agent gets an explicit `mandate`, `productive_bias`, `known_blind_spots`, `preferred_sources`, `escalation_rules`, and `quality_gate`.

This is how the swarm becomes useful. Agents should not be interchangeable prompts.

| Agent | Productive Bias | Quality Gate |
|---|---|---|
| Macro Agent | top-down: rates, FX, liquidity, policy, inflation, crude first | must map macro claim to sectors and instruments |
| Credit Agent | downside-first: spreads, ratings, leverage, funding cost | must cite debt/rating/yield evidence |
| Commodity Agent | input/output spread first | must state who benefits, who loses, and timing uncertainty |
| Equity Catalyst Agent | materiality-first for filings, orders, results, capex | must compare catalyst to company scale and liquidity |
| Derivatives/Hedge Agent | risk-offset-first: futures/options/F&O/basis | must state hedge feasibility and limits |
| Valuation Agent | priced-in skepticism | must compare current valuation to history and peers |
| Market Behavior Agent | price/volume/liquidity confirmation | must flag thin liquidity and flow distortion |
| Risk Review Agent | reject unsupported theses | must list missing evidence and invalidation triggers |

The synthesis agent preserves the tension between these views instead of forcing false consensus.

### Agent Manifest As Code

Agent personality is an execution contract, not branding. Each agent should be configured through a manifest that the router can read.

```json
{
  "agent_id": "commodity_transmission_agent",
  "mandate": "Map commodity shocks to listed beneficiaries and losers.",
  "productive_bias": "Start with input/output spread and inventory cycle.",
  "known_blind_spots": ["ignores valuation unless prompted", "may overstate pass-through speed"],
  "preferred_sources": ["MCX/global commodity feed", "company filings", "sector margin history"],
  "allowed_tools": ["feature_store", "market_graph", "filing_search", "event_study"],
  "context_budget": "small",
  "output_schema": "claim/evidence/confidence/uncertainty/invalidation",
  "quality_gate": "must state who benefits, who loses, timing uncertainty, and evidence IDs",
  "escalation_rules": ["escalate if exposure is material but filing evidence is stale"],
  "stop_rules": ["stop if no listed exposure above materiality threshold"]
}
```

The router uses these manifests to build a task graph. A market situation can therefore activate a small routed set of agents instead of burning tokens across the full 30-40 agent pool.

### 30-40 Agent Scale

Scale through specialist pools:

- sector: defence, railways, power, EMS, IT infrastructure, data centers, capital goods, chemicals, pharma, BFSI, metals, oil/gas, logistics
- event: order wins, results, capex, credit/rating, governance, promoter actions, M&A, regulatory approvals, litigation
- source: BSE, NSE, SEBI, RBI, MoSPI, PIB, tenders, company IR, rating agencies, search/news
- asset class: equity, credit/debt, rates, FX, commodities, derivatives/hedging
- quant: momentum, delivery, liquidity, factor quality, event-study validation, regime detection, peer behavior, hedge simulation
- risk: valuation, balance sheet, governance, execution, crowding, liquidity

Do not run all agents. Route only the needed subset.

```text
situation candidate
-> router
-> selected specialists
-> risk review agents
-> synthesis agent
-> evidence-cited situation brief
```

## 5. Routing Policy

The router chooses agents and models using:

- situation family
- source trust
- evidence freshness
- company sector
- market-cap bucket
- liquidity
- missing fields
- user-facing importance
- model/API budget
- prior agent performance

Example:

| Situation | Activate |
|---|---|
| material order win | filing parser, entity resolver, materiality, price/volume, sector, valuation, risk review, synthesis |
| unexplained accumulation | market behavior, search investigator, exchange-source specialist, sector specialist, risk review |
| policy tailwind | macro/policy, sector specialists, tender mapper, graph builder, search investigator, quant validator |
| MSCI/index event | market-structure specialist, liquidity/flow quant, price/volume, valuation, risk review |
| crude/metal/rate shock | macro shock mapper, sector specialists, exposure graph, price/volume, valuation |

## 6. Deep Research Orchestration Jobs

HIVEMIND should treat complex user prompts as structured research jobs, not as one-shot chat requests.

Example user intent:

```text
Find Indian small/mid-cap stocks with the largest broker target-price upside,
published in a date window, filtered by ROCE, CFO/EBITDA, net debt/equity,
pledge, and earnings-growth guardrails.
```

The AI layer compiles this into a job plan:

```json
{
  "job_type": "forensic_equity_screen",
  "objective": "rank candidates by target-price upside after hard fundamental filters",
  "source_plan": {
    "primary": ["brokerage reports", "exchange filings", "audited earnings"],
    "secondary": ["concall transcripts", "shareholding disclosures", "company presentations"],
    "verification": ["official filings", "broker PDF metadata", "exchange timestamps"]
  },
  "agent_plan": [
    "scope_compiler",
    "universe_builder",
    "source_discovery",
    "broker_target_extractor",
    "earnings_extractor",
    "guardrail_filter",
    "valuation_math",
    "catalyst_agent",
    "risk_review",
    "debate_moderator",
    "synthesis",
    "memory_writer"
  ],
  "ranking": "max((target_price - cmp) / cmp)",
  "stop_rules": [
    "reject if any hard guardrail lacks evidence",
    "reject if target price is stale or not institutionally sourced",
    "mark evidence gap instead of inferring missing values"
  ]
}
```

### Research Job Loop

```text
compile prompt
-> plan sources and agents
-> retrieve official and broker evidence
-> extract structured facts
-> normalize company/security/entity IDs
-> compute formulas
-> apply hard filters
-> run opportunity/risk debate
-> synthesize ranked output
-> store accepted and rejected candidates
-> track future outcome
```

### Debate Pattern For Research Jobs

Do not debate everything. Debate only candidates that pass deterministic filters or have high value but conflicting evidence.

| Debate Role | Question |
|---|---|
| Opportunity Agent | What is the strongest evidence-backed upside case? |
| Valuation Agent | Is the target price mathematically attractive after FY27 estimates? |
| Quality Agent | Do ROCE, cash conversion, debt, pledge, and growth pass hard filters? |
| Risk Agent | Is this a value trap, governance issue, liquidity trap, stale target, or estimate-quality problem? |
| Source Auditor | Are all claims tied to source IDs, dates, and extracted fields? |
| Synthesis Agent | What survives the debate, what is rejected, and what remains uncertain? |

### Knowledge Dump Intake

The system should accept user research prompts, notes, external reports, watchlists, and post-mortems as knowledge artifacts. AI helps convert them into structured assets:

| Input | Stored As | Used For |
|---|---|---|
| user research prompt | research-job template | reusable workflow and agent plan |
| analyst report | raw evidence + extracted thesis | source-backed facts and estimates |
| personal observation | hypothesis artifact | investigation trigger, not truth |
| rejected candidate | negative example | future guardrail and risk training |
| post-mortem | outcome label | agent scorecards and routing improvement |

Knowledge artifacts must keep provenance. A user note or AI conclusion can guide search and routing, but it cannot become a verified fact until linked to evidence.

## 7. Token Optimization Architecture

Heavy AI use is practical only if tokens are routed intelligently.

### Optimization Stack

| Technique | Design Decision |
|---|---|
| deterministic-first extraction | run rules/regex/table parsers before LLMs |
| model cascade | cheap model first; escalate only if confidence is low or value is high |
| prompt caching | cache static agent instructions, source rules, company profiles, sector primers |
| evidence snippets | pass evidence IDs and relevant spans instead of full documents |
| hybrid retrieval | BM25 + dense vector + graph retrieval before any long-context prompt |
| graph context packs | retrieve relevant company-sector-policy-event neighborhoods |
| context compression | compress retrieved evidence while preserving IDs and numeric facts |
| progressive memory | daily/weekly/monthly summaries for old evidence; raw evidence remains available |
| batch extraction | non-urgent jobs run as batch/low-priority calls where providers support it |
| confidence gates | stop early when deterministic confidence is high |
| disagreement gates | run expensive debate only when agents disagree or situation value is high |

### Model Cascade

```text
rules/local parser
-> Qwen/cheap model for classification and extraction
-> DeepSeek Flash for synthesis or first-pass critique
-> DeepSeek Pro/GPT/Gemini only for high-value final reasoning
```

Example:

| Task | First Pass | Escalation |
|---|---|---|
| announcement category | rules + cheap classifier | stronger model if ambiguous |
| order amount extraction | parser + regex | stronger model for messy PDF/table |
| entity resolution | ISIN/alias graph | AI if ambiguous |
| tender-to-company mapping | rules + graph | specialist agent if broad/unclear |
| search query generation | cheap model | stronger only for high-priority unexplained move |
| final brief | compressed agent outputs | strongest available reasoning model |

## 8. Memory And Retrieval

The AI layer should use a hybrid memory system:

| Memory | Storage | Purpose |
|---|---|---|
| Working memory | in-process/context object | current run state and agent outputs |
| Recent memory | Redis/Postgres | recent situations, source status, watchlists |
| Semantic memory | Qdrant/vector store | similar filings, theses, situations, research notes |
| Lexical memory | Postgres full-text/BM25 | exact terms, tickers, tender IDs, policy names |
| Graph memory | Neo4j/Postgres graph tables | company-sector-policy-tender-customer-event relationships |
| Outcome memory | Postgres | post-mortems, abnormal returns, false positives, agent performance |

### Storage Boundary Rules

Do not treat vector memory as the primary database. It is a semantic index.

| Data Type | Primary Home | Secondary Index |
|---|---|---|
| raw filings, broker PDFs, pages, RSS, API payloads | evidence lake/object storage | optional text chunks in vector store |
| extracted financial facts and tables | Postgres/DuckDB/Parquet | BM25/vector for retrieval |
| market data and features | feature store/time-series tables | summary embeddings only if useful |
| entity and exposure relationships | graph tables/Neo4j | GraphRAG context packs |
| agent outputs and costs | agent_run tables | vector only for similar prior reasoning |
| post-mortems and outcome labels | outcome tables | graph edges and retrieval examples |

Every vector chunk must include:

- evidence ID or derived record ID
- source URL/path
- source timestamp and fetch timestamp
- parser/model version
- chunk text hash
- entity links
- permission/license class

Every graph edge must include:

- edge type
- source evidence ID
- extraction method
- confidence
- valid-from/valid-to when known
- version and last-verified timestamp

### Making Agents Smarter Without Fine-Tuning

The first learning mechanism is not model fine-tuning. It is memory-assisted orchestration.

```text
past evidence + similar situations + outcome labels + agent scorecards
-> better context packs
-> better agent selection
-> better critique checklists
-> better thresholds
-> better final synthesis
```

Fine-tuning can come later for narrow tasks such as extraction, classification, and risk-review style imitation, but the MVP should learn through retrieval, routing, and post-mortem feedback first.

Retrieval pipeline:

```text
task query
-> query rewriting
-> BM25 + vector + graph retrieval
-> reciprocal-rank fusion
-> rerank
-> context compression
-> agent context pack with evidence IDs
```

## 9. GraphRAG Pattern

HIVEMIND should use graph retrieval for questions like:

- Which companies benefit from a policy/tender category?
- Which customers and ministries are connected to this company?
- Which companies had similar order wins and what happened later?
- Which sectors have positive/negative exposure to crude, metals, rates, FX, or geopolitical shocks?
- Which passive-flow events have historically moved low-liquidity names?

Graph node types:

- Instrument
- Company
- Sector
- Theme
- Customer
- Ministry
- Tender
- CorporateEvent
- PolicyEvent
- MacroShock
- MarketStructureEvent
- PriceBehavior
- ValuationSnapshot
- Situation
- AgentRun
- OutcomeLabel

Key edges:

- `LISTED_AS`
- `BELONGS_TO_SECTOR`
- `HAS_THEME_EXPOSURE`
- `SUPPLIES_TO`
- `DISCLOSED_EVENT`
- `MENTIONED_IN`
- `BENEFITS_FROM`
- `HURT_BY`
- `CONFIRMED_BY_PRICE`
- `HAS_VALUATION_CONTEXT`
- `SIMILAR_TO`
- `LED_TO_OUTCOME`
- `CREATED_BY_AGENT`

## 10. Agent Output Contract

Every agent returns structured JSON:

```json
{
  "agent": "market_behavior_agent",
  "task": "interpret_price_volume_context",
  "finding": "Volume expansion confirms attention, but follow-through is not yet proven.",
  "confidence": 0.74,
  "evidence_ids": ["PRICE_2026_05_29", "DELIVERY_2026_05_29"],
  "features_used": ["volume_zscore", "relative_strength_5d", "delivery_pct"],
  "uncertainties": ["no intraday depth feed available"],
  "next_actions": ["check delivery follow-through for 3 sessions"],
  "cost": {
    "input_tokens": 1800,
    "output_tokens": 250,
    "provider": "qwen",
    "model": "qwen-flash"
  }
}
```

The risk reviewer rejects:

- claims without evidence IDs
- invented numbers
- stale source assumptions
- source-quality confusion
- buy/sell certainty from weak evidence
- final briefs that hide uncertainty

## 11. Synthesis Agent

The final output is a situation brief, not an automated trade call.

```json
{
  "situation_type": "material_order_win_rerating",
  "instrument": "Example Ltd",
  "conviction": "medium_high",
  "evidence_strength": "high",
  "market_confirmation": "present_but_early",
  "valuation_context": "fair_with_confirmation",
  "bull_case": "...",
  "bear_case": "...",
  "why_now": "...",
  "what_can_go_wrong": "...",
  "missing_information": ["project duration", "margin profile"],
  "next_actions": ["track delivery follow-through", "check management commentary"],
  "evidence_ids": ["EV_1", "EV_2", "PRICE_1"]
}
```

The synthesis agent must preserve uncertainty. If the opportunity agent is constructive and the risk reviewer flags valuation/crowding, the brief should show both.

## 12. Quant And Reasoning Configuration

Reasoning settings should depend on task type:

| Task | Reasoning Style | Temperature | Notes |
|---|---|---|---|
| extraction/classification | strict schema | low | JSON validation, retries, no creativity |
| search query generation | divergent but bounded | medium | multiple query families, date-aware |
| sector mapping | evidence-grounded reasoning | low/medium | preserve uncertainty |
| bull/bear debate | adversarial | medium | separate roles, no unsupported claims |
| quant validation | deterministic + explanation | low | show method, inputs, windows |
| final brief | synthesis | low/medium | concise, cited, uncertainty visible |

Use self-consistency or multi-sample reasoning only for high-value ambiguous situations because it multiplies cost.

## 13. Evaluation

AI metrics:

- extraction accuracy
- entity-resolution accuracy
- schema-valid output rate
- evidence-grounding rate
- hallucination rate
- uncertainty preservation
- risk-review catch rate
- cost per situation

Finance/system metrics:

- missed-catalyst rate
- false-positive rate by situation family
- abnormal return by event window
- precision of attention queue
- post-mortem learning rate
- source freshness and outage time
- cost per useful alert

## 14. Implementation Sequence

1. `AIModelProvider` interface and `MockProvider`
2. model-run audit table
3. evidence-context pack schema
4. cheap extraction agent for filings
5. entity resolver agent
6. search investigator agent
7. graph writer agent
8. market behavior agent
9. risk review agent
10. synthesis agent
11. model router and cost budget
12. progressive context compression
13. specialist pools
14. agent performance and post-mortem feedback

## 15. Practical Provider Strategy

Use whatever APIs are available without coupling the product to them:

- Qwen Flash: bulk cheap extraction/classification where available
- DeepSeek V4 Flash: cheap synthesis, first-pass critique, broad research
- DeepSeek V4 Pro: final high-value reasoning only
- Gemini/OpenAI: fallback or strongest-available tasks when keys/credits exist
- local/open-weight models: offline tests, embeddings, classification, compression

The architecture should survive API price changes because routing and provider adapters are separate from agent logic.
