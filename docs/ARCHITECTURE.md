# HIVEMIND Market Intelligence Architecture

Status: Theory and system design draft  
Audience: Founder, product, quant, backend, AI engineering  
Mode: Free-first, swing-trading intelligence, small/mid-cap focused  

## 1. Core Problem

The goal is not to build another stock screener.

The goal is to build a system that notices when a listed company is becoming important before the opportunity is obvious to everyone.

Examples:

- Dynacons-style move: company-specific order win, large relative to company size
- MTAR-style move: sector/theme strength plus company-specific positioning
- unexplained price run: price and volume move first, reason appears later
- policy-driven move: government allocation or regulation creates a sector tailwind
- tender-driven move: procurement activity points toward future order winners

These moves are missed when the system only looks at one data type.

A price-only screener misses the reason.

A news-only screener misses accumulation before the news.

An AI-only system hallucinates or reacts late.

A generic ranker treats all signals equally and loses the context that makes small/mid-cap moves powerful.

HIVEMIND should work differently.

It should build a living evidence graph around every company and theme, then identify when evidence, timing, materiality, and market behavior start reinforcing each other.

## 2. Design Principle

HIVEMIND is an evidence-first intelligence system.

It does not ask:

> Which stock has the highest score?

It asks:

> What changed, who benefits, how material is it, is the market confirming it, and what evidence supports that view?

This distinction matters.

A generic signal system produces alerts like:

```text
Stock up 8 percent on high volume.
```

HIVEMIND should produce something closer to:

```text
Company received a large government-linked digital infrastructure order.
Order size appears material relative to company scale.
The stock is small/mid-cap, so incremental order flow may affect perception faster.
Volume expanded after the disclosure.
The event also matches a broader digital infrastructure tailwind.
Evidence confidence is high because the source is an exchange filing.
```

The second alert is not just a signal. It is a thesis seed.

## 3. Why Generic Signals Fail

Generic signals fail because they flatten very different situations into the same score.

Example:

| Situation | Generic Signal View | HIVEMIND View |
|---|---|---|
| Large-cap stock rises 3 percent on result day | positive price action | maybe normal noise |
| Small-cap wins order equal to large share of annual revenue | positive news | potentially thesis-changing |
| Stock breaks out before news | technical breakout | unexplained accumulation requiring investigation |
| Budget boosts railway capex | macro news | sector graph update affecting vendors |
| Tender award appears before company filing | public procurement item | early order pipeline clue |

The same price move can mean different things depending on company size, sector, liquidity, source quality, market regime, and whether the event changes future expectations.

So HIVEMIND should not rely on generic signal names.

It should model **situations**.

## 4. The Situation Model

A situation is a structured interpretation of what may be happening around a company.

Every situation has:

- trigger
- evidence
- company context
- market behavior
- sector/theme context
- materiality
- uncertainty
- time horizon

Example:

```json
{
  "situation_type": "material_order_win_small_mid_cap",
  "company": "Dynacons Systems and Solutions",
  "trigger": "exchange_announcement",
  "event": "order_win",
  "amount_inr_cr": 750,
  "materiality_basis": ["order_size_vs_market_cap", "order_size_vs_revenue"],
  "market_behavior": ["volume_expansion", "price_breakout"],
  "tailwinds": ["government_it_spend", "digital_infrastructure"],
  "evidence_quality": "official",
  "uncertainty": ["execution_margin_unknown", "project_duration_unknown"],
  "time_horizon": "days_to_months"
}
```

This is not a stock score. It is a machine-readable thesis object.

## 5. The Six Intelligence Lanes

HIVEMIND should process the market through six separate intelligence lanes.

Each lane answers a different question.

### Lane 1: Official Corporate Events

Question:

> Did the company disclose something that can change expectations?

Sources:

- BSE announcements
- NSE announcements
- company investor relations pages
- rating agency releases
- exchange corporate actions

Events:

- order win
- contract extension
- tender win
- result growth
- margin expansion
- debt reduction
- rating upgrade
- capex
- fundraise
- promoter action
- regulatory approval
- litigation/risk disclosure

Why this lane matters:

Official disclosures are the strongest evidence source. For small and mid caps, a single announcement can change the market's view of the company.

Non-generic logic:

An order win is not automatically bullish.

The system must ask:

- Is the value disclosed?
- Is the value large relative to market cap?
- Is the value large relative to trailing revenue?
- Is the customer credible?
- Is the order repeatable or one-off?
- Is it high-margin or low-margin work?
- Is there execution risk?
- Did volume confirm after disclosure?

### Lane 2: Price, Volume, Delivery, and Liquidity Behavior

Question:

> Is the market behaving as if something has changed?

Sources:

- NSE/BSE bhavcopy
- delivery data
- EOD OHLCV
- corporate action adjusted history

Signals:

- volume expansion
- delivery spike
- breakout
- relative strength
- multi-day accumulation
- low-float sharp move
- sector-relative move
- unexplained gap

Why this lane matters:

Some moves start before the clean reason is visible. Small and mid caps often show accumulation before broad public attention.

Non-generic logic:

A price spike is not the alert.

A price spike is a question:

> What explains this?

For every unusual move, the system should launch an investigation:

- check exchange filings
- check recent tenders
- check sector news
- check company news
- check peer moves
- check macro/policy events
- check whether the move is isolated or sector-wide

If no reason is found, the situation becomes:

```text
unexplained_price_action_under_investigation
```

This is still useful because unexplained strength can precede a catalyst.

### Lane 3: Macro and Policy Tailwinds

Question:

> Did a policy, regulation, budget, or macro change improve the future environment for a sector?

Sources:

- RBI
- SEBI
- MoSPI/eSankhyiki
- PIB
- union budget documents
- ministry releases
- cabinet approvals
- sector regulator releases

Tailwinds:

- defence procurement
- railway capex
- digital infrastructure
- data centers
- PLI schemes
- renewable energy
- power transmission
- semiconductor/electronics
- import duty changes
- export incentives
- interest rate changes
- liquidity changes

Why this lane matters:

Some stocks move because the market starts repricing the future of a whole sector.

Non-generic logic:

Policy news is not directly a stock signal.

It must pass through a beneficiary graph:

```text
policy event
-> sector
-> sub-sector
-> business activity
-> listed companies
-> revenue exposure
-> order history
-> price confirmation
```

Example:

```text
railway capex increase
-> railway infrastructure
-> signalling, cables, EPC, rolling stock, electronics
-> listed vendors and suppliers
-> companies with railway order history
-> watch for filings, tender wins, price-volume strength
```

### Lane 4: Tender and Procurement Pipeline

Question:

> Are future orders forming before they appear in company announcements?

Sources:

- CPPP/eProcure
- GeM
- IREPS
- PSU procurement portals
- defence procurement
- state tenders
- power utility tenders
- infrastructure tender portals

Events:

- new tender
- tender amendment
- bid deadline
- L1 result
- award notice
- repeat bidder activity
- procurement plan

Why this lane matters:

Tenders can show demand before the listed company announces a win.

Non-generic logic:

A tender is not automatically relevant to a stock.

The system should ask:

- Which sector does this tender belong to?
- Which listed companies can technically qualify?
- Have they won similar tenders before?
- Is the tender size meaningful?
- Is the buyer a credible government/PSU/large enterprise?
- Is this a one-off tender or part of a bigger spending wave?

This lane creates early watchlists rather than final buy signals.

### Lane 5: News and Search Discovery

Question:

> Is there relevant public context that official sources did not make easy to find?

Sources:

- search engines
- business news
- sector media
- company press releases
- local news
- government release mirrors
- trade publications

Search engines are not the truth layer.

They are useful for:

- investigating unexplained price action
- discovering missed company news
- finding tender/result/order context
- checking sector narratives
- finding local or trade-publication coverage
- daily missed-event audit

Non-generic logic:

Search should be task-driven, not broad scraping.

Bad approach:

```text
Search the web for all stock news.
```

Good approach:

```text
Stock moved unusually.
Generate targeted queries from company, aliases, sector, recent filings, and keywords.
Collect candidate pages.
Classify source quality.
Verify against official filings where possible.
Store all evidence.
```

Example query families:

```text
"Dynacons Systems" order
"Dynacons Systems" contract
"Dynacons Systems" tender
"Dynacons Systems" government project
"Dynacons Systems" BSE announcement
"Dynacons Systems" investor presentation
```

For MTAR-style investigation:

```text
"MTAR" defence order
"MTAR" space
"MTAR" nuclear
"MTAR" clean energy
"MTAR" order book
"MTAR" ISRO
```

The search lane should be activated by context:

- price anomaly
- company on watchlist
- policy tailwind
- tender category match
- missing evidence
- end-of-day audit

### Lane 6: Fundamentals and Business Quality

Question:

> Is this company capable of turning the event/tailwind into real value?

Sources:

- results
- annual reports
- investor presentations
- shareholding patterns
- rating reports
- balance sheet data
- order book disclosures

Features:

- revenue growth
- margin trend
- debt trend
- promoter holding
- pledge risk
- working capital pressure
- order book quality
- customer concentration
- valuation regime

Why this lane matters:

A strong event in a weak company can still produce a trade, but conviction should be different from a strong event in an improving company.

Non-generic logic:

HIVEMIND should separate:

- trade catalyst
- business quality
- execution risk
- valuation risk

This prevents the system from confusing "stock can move" with "company is fundamentally strong".

## 6. Evidence Graph

The central data structure should be an evidence graph.

Not just tables. Not just embeddings. Not just a search index.

The graph connects:

```text
company
-> exchange listings
-> aliases
-> sectors
-> products
-> customers
-> tenders
-> announcements
-> policy tailwinds
-> peers
-> price behavior
-> historical situations
```

Example:

```text
Dynacons Systems
-> IT infrastructure
-> digital transformation
-> government IT spend
-> order wins
-> BSE/NSE filings
-> price-volume response
-> similar past events
```

Example:

```text
MTAR
-> precision engineering
-> space
-> defence
-> nuclear
-> clean energy
-> strategic manufacturing
-> policy/tender/order-book sensitivity
```

This graph is what makes the system non-generic.

The system does not just see "news". It sees:

```text
news connected to a sector
sector connected to policy
policy connected to tenders
tenders connected to companies
companies connected to price behavior
```

## 7. Situation Engines

Instead of one ranking model, HIVEMIND should have multiple situation engines.

Each engine detects a different pattern.

### Engine A: Material Order-Win Engine

Detects:

- official order win
- contract value disclosed
- company is small/mid cap
- value is large versus company size
- credible customer
- volume/price confirmation

Output:

```text
material_order_win_small_mid_cap
```

### Engine B: Sector Tailwind Engine

Detects:

- macro/policy/tender wave
- specific sector or sub-sector impact
- listed beneficiaries
- historical exposure
- early price action among beneficiaries

Output:

```text
sector_tailwind_candidate
```

### Engine C: Unexplained Price Action Engine

Detects:

- abnormal price/volume/delivery move
- no immediate official explanation
- search/news/tender investigation triggered

Output:

```text
unexplained_price_action_under_investigation
```

### Engine D: Tender Pipeline Engine

Detects:

- tender or procurement event
- possible listed beneficiaries
- high-value opportunity
- repeat category or buyer

Output:

```text
tender_pipeline_watchlist
```

### Engine E: Result Re-Rating Engine

Detects:

- revenue growth
- margin expansion
- guidance/order book improvement
- price breakout
- sector confirmation

Output:

```text
earnings_rerating_candidate
```

### Engine F: Theme Rotation Engine

Detects:

- multiple stocks in same theme moving
- news/policy/tender catalyst
- leader/laggard behavior
- small/mid-cap participation

Output:

```text
theme_rotation_detected
```

## 8. Alert Philosophy

HIVEMIND alerts should not say:

```text
Buy stock X.
```

They should say:

```text
Investigate stock X because situation Y is forming.
Evidence strength is high/medium/low.
Materiality appears high/medium/low.
Market confirmation is present/absent.
Main uncertainty is Z.
```

Alert structure:

```json
{
  "company": "Example Ltd",
  "situation_type": "material_order_win_small_mid_cap",
  "time_horizon": "days_to_months",
  "evidence_strength": "high",
  "materiality": "high",
  "market_confirmation": "partial",
  "tailwind_alignment": "strong",
  "why_now": "...",
  "why_it_matters": "...",
  "what_can_go_wrong": "...",
  "evidence": ["exchange filing", "price-volume data", "policy release"]
}
```

This keeps the system useful for swing trading while avoiding false certainty.

## 9. Scoring Without Becoming Generic

The system can still use scores, but scores should be situation-specific.

Do not create one universal "stock score" first.

Instead:

```text
order_win_score
tailwind_score
price_action_score
tender_pipeline_score
result_rerating_score
theme_rotation_score
```

Then create a final attention priority:

```text
attention_priority = max/smart_fusion(situation_scores)
```

Why this matters:

A stock can be uninteresting fundamentally but still have a powerful order-win situation.

Another stock can have no corporate news but be important because the entire sector is rotating.

Another can be a search candidate only because price action is unusual.

These should not be forced into one flat model too early.

## 10. Processing Strategy for Massive Data

The system should not process every source with the same intensity.

Use a tiered processing model.

### Tier 0: Universe Refresh

Frequency:

- daily or weekly

Purpose:

- maintain listed company universe
- update aliases
- map NSE/BSE/ISIN
- update sector and market-cap bucket

### Tier 1: High-Trust Event Polling

Frequency:

- every few minutes to hourly during market days
- EOD catch-up

Sources:

- BSE announcements
- NSE announcements
- SEBI RSS
- important ministry/PIB feeds

Processing:

- fetch
- dedupe
- store raw evidence
- parse event
- map company
- create situation candidate

### Tier 2: Price/Volume Scan

Frequency:

- EOD for first version
- later intraday snapshots if free sources support it

Processing:

- detect abnormal moves
- trigger investigation only for unusual stocks
- avoid searching the whole market blindly

### Tier 3: Tailwind and Tender Watch

Frequency:

- daily
- higher frequency for tracked ministries/sectors

Processing:

- detect policy/tender events
- map to sectors
- update theme graph
- watch beneficiary companies

### Tier 4: Search and News Investigation

Frequency:

- triggered, not constant

Triggers:

- unexplained price action
- major policy event
- tender category match
- company enters watchlist
- duplicate/missing evidence
- EOD missed-move audit

This makes search smart and cheap.

## 11. Smart Search Engine Use

Search should be an investigation tool.

Search workflow:

1. Generate query set from company aliases, sector, event suspicion, and date range.
2. Fetch top results from multiple search sources where possible.
3. Store result page metadata.
4. Classify source quality.
5. Extract candidate evidence.
6. Verify against official source if possible.
7. Attach findings to a situation.

Source quality levels:

| Level | Source | Use |
|---|---|---|
| A | exchange/regulator/government/company | truth source |
| B | reputed financial media/rating agency | strong context |
| C | sector/trade/local media | discovery |
| D | social/forums/SEO aggregators | weak clue only |

Search should produce:

```text
candidate_evidence
```

not:

```text
final_truth
```

## 12. AI Role

AI is the analyst assistant inside the pipeline.

AI should:

- read messy PDFs
- classify events
- extract order value/customer/timeline
- map policy to sectors
- map tender descriptions to possible listed companies
- cluster duplicate articles
- explain situations
- generate investigation queries
- identify missing information

AI should not:

- invent data
- replace price feeds
- replace exchange filings
- create unsupported claims
- make final decisions without evidence

AI outputs must include:

- source evidence id
- extracted fields
- confidence
- uncertainty
- evidence quote or reference
- reason for classification

## 13. AI Swarm Fusion Layer

The AI swarm should be fused into HIVEMIND after evidence capture, event parsing, and situation generation.

The swarm is not the data source.

The swarm is the reasoning committee.

```text
raw sources
-> raw evidence store
-> structured events
-> company/sector/tailwind graph
-> situation engines
-> AI swarm
-> final situation brief
```

This separation is important because the system needs two different kinds of intelligence:

- data intelligence: what happened, where it came from, and whether it is trustworthy
- reasoning intelligence: what it may mean, why it matters, what can go wrong, and what to investigate next

The AI swarm belongs to the second layer.

### Swarm Activation

The swarm should not run on every company every day.

It should activate only when a situation deserves deeper reasoning:

- official high-materiality event
- abnormal price/volume move
- unexplained price action
- new macro/policy/tender tailwind
- tender linked to listed beneficiaries
- small/mid-cap with sudden attention
- conflicting evidence
- end-of-day review of top candidates

This keeps cost and noise under control.

### Swarm Agents

The first version should use these agents:

| Agent | Role | Output |
|---|---|---|
| Event Extraction Agent | Extracts event type, value, customer, timeline, source confidence | structured event patch |
| Company Context Agent | Checks company size, business model, order history, customer exposure | materiality view |
| Sector Tailwind Agent | Maps macro/policy/tender events to sectors and beneficiaries | tailwind view |
| Price/Volume Agent | Interprets market confirmation and accumulation behavior | market behavior view |
| Search Investigator Agent | Investigates missing context and unexplained moves | candidate evidence |
| Bull Case Agent | Builds the positive thesis from evidence | bull thesis |
| Bear/Critic Agent | Challenges the thesis and identifies risk | risk thesis |
| Fusion Judge | Combines agent outputs into one situation brief | final brief |

### Swarm Fusion Output

The swarm should produce a final situation brief, not a buy/sell call.

```json
{
  "company": "Example Ltd",
  "situation_type": "material_order_win_small_mid_cap",
  "conviction": "medium_high",
  "evidence_strength": "high",
  "market_confirmation": "present",
  "tailwind_alignment": "strong",
  "why_it_matters": "...",
  "what_can_go_wrong": "...",
  "missing_information": ["project duration", "margin profile"],
  "next_actions": ["track follow-through volume", "check management commentary"],
  "sources": ["exchange filing", "price-volume data"]
}
```

The Fusion Judge must preserve disagreement.

If the Bull Case Agent is positive but the Bear/Critic Agent finds execution risk or valuation risk, the final brief should show that tension clearly.

## 14. Model-Agnostic AI Layer

The AI layer must be model agnostic from day one.

For now, HIVEMIND may only have a few API keys available. Later, the project may use Gemini, GPT, local models, open-source hosted models, or multiple providers at once.

Therefore, no agent should depend directly on a specific provider SDK.

Every agent should depend on a common model interface.

### Provider Abstraction

```python
class AIModelProvider:
    name: str

    def generate(self, request: AIRequest) -> AIResponse:
        ...

    def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        ...
```

The provider can be:

- Gemini
- OpenAI GPT
- Anthropic
- local model
- open-source hosted model
- mock model for testing

Agents should not know which provider is being used.

### Agent Interface

```python
class Agent:
    name: str
    role: str

    def run(self, context: AgentContext, model: AIModelProvider) -> AgentResult:
        ...
```

The agent receives:

- situation candidate
- evidence bundle
- company context
- sector/tailwind context
- price/volume context
- task instructions

The agent returns:

- structured findings
- confidence
- citations/evidence ids
- uncertainty
- recommended next action

### Model Routing

HIVEMIND should support model routing later.

Example:

| Task | Preferred Model Type |
|---|---|
| cheap classification | small fast model |
| PDF summarization | long-context model |
| extraction with schema | reliable structured-output model |
| final reasoning brief | strongest available reasoning model |
| embeddings | embedding-specific model |
| tests/local dev | mock provider |

For now, we can keep this simple:

```text
agent -> configured default provider
```

Later:

```text
agent + task + cost budget + latency need -> provider router -> model
```

### Prompt Portability

Prompts should be written as provider-neutral task specs.

Avoid provider-specific assumptions like:

- only one vendor's JSON mode
- tool-calling format locked to one API
- model-specific system prompt behavior
- provider-specific safety or citation features

Use a common internal format:

```json
{
  "task": "classify_market_event",
  "instructions": "...",
  "evidence": [...],
  "required_schema": {...},
  "output_contract": "strict_json"
}
```

Then provider adapters translate this request into Gemini/OpenAI/local-model calls.

### Evidence Contract

Every AI agent must receive evidence ids, not just plain text.

Every AI result must cite the evidence ids it used.

```json
{
  "finding": "The announcement appears to be a material order win.",
  "confidence": 0.86,
  "evidence_ids": [101, 102],
  "uncertainty": ["margin profile not disclosed"]
}
```

This keeps AI useful without allowing unsupported claims.

### Model-Agnostic Storage

AI outputs should store:

- provider name
- model name
- prompt version
- input evidence ids
- output JSON
- confidence
- created_at

This allows the same situation to be re-run later with a better model.

The system should support:

```text
reprocess situation with stronger model
compare model outputs
audit old AI reasoning
upgrade prompts without changing raw evidence
```

### First Implementation Rule

Do not build Gemini-specific or GPT-specific agents.

Build:

```text
Agent -> AIModelProvider interface -> concrete provider adapter
```

Initial providers:

- `MockProvider` for development
- `GeminiProvider` when key is available
- `OpenAIProvider` when key is available

This lets HIVEMIND progress even before all API keys are ready.

## 15. Example: Dynacons-Style Flow

1. BSE/NSE announcement fetched.
2. Raw evidence stored.
3. Parser detects order-win language.
4. Amount extractor finds `750 crore`.
5. Entity resolver maps company to listed instrument.
6. Materiality engine compares order value to company scale.
7. Tailwind graph maps event to digital infrastructure/government IT.
8. Price/volume lane checks market confirmation.
9. Situation engine emits:

```text
material_order_win_small_mid_cap
```

10. Alert explains:

```text
This is not just news. It is a potentially material company-specific catalyst with policy/tailwind alignment and market confirmation.
```

Then the AI swarm activates:

1. Event Extraction Agent verifies order value and event type.
2. Company Context Agent checks whether the order is material relative to the company.
3. Sector Tailwind Agent maps it to digital infrastructure/government IT.
4. Price/Volume Agent checks confirmation.
5. Bear/Critic Agent checks execution risk, margin uncertainty, and whether news is already priced.
6. Fusion Judge produces the final situation brief.

The model used by each agent can be Gemini, GPT, local, or mock. The agent logic remains the same.

## 16. Example: MTAR-Style Flow

1. Policy/tailwind lane detects defence/space/nuclear/clean-energy strength.
2. Graph maps MTAR to precision engineering and strategic manufacturing themes.
3. Price/volume lane detects relative strength.
4. Search lane investigates recent order book, sector commentary, and filings.
5. Fundamentals lane checks order book, margins, and customer concentration.
6. Situation engine emits:

```text
strategic_manufacturing_tailwind_with_market_confirmation
```

This is different from Dynacons.

Dynacons is event-led.

MTAR may be theme-led plus market-confirmed.

The architecture must support both.

The AI swarm handles this differently from Dynacons:

- Sector Tailwind Agent becomes more important.
- Company Context Agent checks strategic manufacturing exposure.
- Price/Volume Agent checks whether the market is confirming the theme.
- Search Investigator Agent looks for recent order book, customer, or sector developments.
- Fusion Judge decides whether this is theme-led, event-led, or price-led.

## 17. Final Architecture

```mermaid
flowchart TD
    universe["Instrument Universe\nNSE/BSE small + mid caps, SME optional"] --> raw_sources

    raw_sources["Raw Source Layer"] --> official["Official Events\nBSE/NSE/company/regulator"]
    raw_sources --> market["Market Data\nprice/volume/delivery"]
    raw_sources --> macro["Macro + Policy\nRBI/SEBI/MoSPI/PIB"]
    raw_sources --> tenders["Tender + Procurement\nCPPP/GeM/PSU/sector portals"]
    raw_sources --> search["Search + News Discovery\ntriggered investigation"]

    official --> evidence["Raw Evidence Store"]
    market --> evidence
    macro --> evidence
    tenders --> evidence
    search --> evidence

    evidence --> normalize["Normalization + Deduplication"]
    normalize --> events["Structured Events"]
    normalize --> price_features["Price/Volume Features"]
    normalize --> tailwinds["Tailwind Events"]

    events --> graph["Company-Sector-Policy-Tender Graph"]
    price_features --> graph
    tailwinds --> graph

    graph --> situations["Situation Engines"]

    situations --> swarm["AI Swarm Reasoning Layer"]
    swarm --> agents["Model-Agnostic Agents"]
    agents --> provider["AIModelProvider Interface"]
    provider --> gemini["Gemini Provider"]
    provider --> gpt["GPT Provider"]
    provider --> local["Local/Open Provider"]
    provider --> mock["Mock Provider"]

    agents --> fusion["Fusion Judge"]
    fusion --> briefs["Situation Briefs"]
    fusion --> alerts["Watchlist / Alert Queue"]
    fusion --> research["Investigation Queue"]
```

Layer responsibility:

| Layer | Responsibility |
|---|---|
| Raw Source Layer | Fetch data from official, market, macro, tender, and search sources |
| Raw Evidence Store | Preserve immutable evidence before AI or parsing changes it |
| Normalization | Deduplicate, parse, clean, and map records |
| Graph | Connect companies, sectors, policies, tenders, peers, and price behavior |
| Situation Engines | Detect specific market situations |
| AI Swarm | Reason over evidence and produce thesis/risk/context |
| Model Provider Interface | Keep all agents model agnostic |
| Fusion Judge | Combine agent views into one final situation brief |
| Output Layer | Alerts, watchlists, briefs, research queue |

## 18. First Build Sequence

Build in this order:

1. Instrument universe
2. Raw evidence store
3. BSE/NSE announcement ingestion
4. Event parser for order wins/results/capex/rating/promoter activity
5. EOD price-volume scanner
6. Unexplained price-action investigation queue
7. Search engine investigation lane
8. Macro/policy ingestion
9. Sector/company/tailwind graph
10. Tender lane
11. Model-agnostic AI provider interface
12. MockProvider for local development
13. AI extraction and explanation agents
14. Swarm Fusion Judge
15. Situation engines and alert fusion

## 19. What Makes HIVEMIND Different

HIVEMIND is not:

- a stock screener
- a news scraper
- a price-action bot
- a generic AI analyst
- a single ranking model

HIVEMIND is:

- an evidence capture system
- a market-change detector
- a situation engine
- a company-sector-policy graph
- an investigation assistant
- a swing-trading attention system

The output is not "top stocks".

The output is:

```text
Here are the situations forming in the market.
Here is the evidence.
Here is why they may matter.
Here is what is still uncertain.
Here is where your attention should go first.
```
