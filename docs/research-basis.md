# HIVEMIND Research Basis

Status: current synthesis as of 2026-05-30  
Purpose: turn AI, quant, data engineering, and market-data research into concrete design decisions

## 1. What We Learned

HIVEMIND should be pitched and built as an AI-swarm capital-markets intelligence terminal.

The strongest design is not:

```text
data -> one model -> generic market score
```

It is:

```text
evidence -> graph/memory -> situation engines -> routed AI specialists -> quant validation -> synthesis brief
```

The strongest investor positioning is:

```text
professional capital-markets workflow + agentic investigation + cross-asset evidence graph
```

Bloomberg is the familiar reference for an integrated market terminal: data, news, analytics, research, and workflow in one environment. HIVEMIND's difference is that the intelligence layer is agentic and replayable across shares/equities, debt, commodities, FX, rates, derivatives, policy, flows, and fundamentals. Every terminal screen can call source agents, search agents, macro agents, credit agents, commodity agents, derivatives/hedge agents, quant validators, risk reviewers, and a synthesis agent.

## 2. AI Swarm And Agent Research

| Research / Technique | What It Says | HIVEMIND Decision |
|---|---|---|
| AutoGen | Microsoft describes multi-agent applications built from conversational agents and tooling. | Use an orchestrator/router with specialist agents, tools, and evidence contracts. |
| Magentic-One | Microsoft presents a generalist multi-agent system with an orchestrator coordinating specialist agents. | Use a strong router/orchestrator and specialized agents for source, market, sector, quant, risk, and synthesis work. |
| CAMEL | Communicative agents can create scalable role-based agent societies. | Give agents explicit roles, not generic prompts. |
| AgentScope | Multi-agent systems need message exchange, scale, and robust runtime design. | Treat agents as workers in an execution graph with audit logs, not ad hoc chats. |
| Mixture-of-Agents | Layered agents can improve final response quality by synthesizing outputs from previous agents. | Use layered research: extraction agents, specialist agents, risk review, then synthesis agent. |
| Anthropic agent workflows | Production agent systems work best when patterns such as routing, orchestrator-workers, and evaluator-optimizer are used deliberately. | Route tasks by situation type; use evaluator/review agents where quality matters. |
| OpenAI Swarm | OpenAI's educational framework demonstrates lightweight agent handoffs and orchestration concepts. | Keep agent handoffs simple, auditable, and model agnostic; do not depend on one framework. |
| FinDebate | Recent finance-agent research uses earnings, market, sentiment, valuation, and risk specialists with debate to improve financial analysis. | Make opportunity/risk/valuation disagreement visible in the terminal. |
| P1GPT | Multi-agent financial workflows can fuse technical, fundamental, and news signals into interpretable rationales. | Build situation pages that combine market behavior, fundamentals, filings, macro, credit, commodities, derivatives context, and news evidence. |
| iMAD / debate research | Debate is useful when selectively triggered; running debate on everything wastes tokens and can degrade answers. | Use swarm debate only for high-value, ambiguous, or high-impact situations. |
| ReAct | Reasoning should be interleaved with actions/tool use. | Agents should retrieve, inspect, call tools, and update findings rather than summarize one static prompt. |
| Reflexion | Agents can improve using verbal feedback from mistakes. | Store post-mortems and inject recent failure lessons into future agent runs. |
| Tree of Thoughts / Graph of Thoughts | Complex reasoning benefits from exploring multiple reasoning paths. | Use multi-branch opportunity/risk/review reasoning only for high-value ambiguous situations. |

Key links:

- Bloomberg Terminal: https://www.bloomberg.com/professional/products/bloomberg-terminal/
- AutoGen: https://www.microsoft.com/en-us/research/blog/autogen-enabling-next-generation-large-language-model-applications/
- AutoGen paper: https://arxiv.org/abs/2308.08155
- Magentic-One: https://www.microsoft.com/en-us/research/articles/magentic-one-a-generalist-multi-agent-system-for-solving-complex-tasks/
- CAMEL: https://arxiv.org/abs/2303.17760
- AgentScope: https://arxiv.org/abs/2402.14034
- Mixture-of-Agents: https://arxiv.org/abs/2406.04692
- Anthropic effective agents: https://www.anthropic.com/engineering/building-effective-agents
- OpenAI Swarm: https://github.com/openai/swarm
- FinDebate: https://arxiv.org/abs/2509.17395
- P1GPT: https://arxiv.org/abs/2510.23032
- iMAD: https://arxiv.org/abs/2511.11306
- ReAct: https://arxiv.org/abs/2210.03629
- Reflexion: https://arxiv.org/abs/2303.11366
- Tree of Thoughts: https://arxiv.org/abs/2305.10601

## 3. RAG, Graph Memory, And Search Research

| Research / Technique | What It Says | HIVEMIND Decision |
|---|---|---|
| Microsoft GraphRAG | Graph-based indexing and community summaries help answer global questions over large corpora where naive RAG struggles. | Build a company-sector-policy-tender-event graph and use graph retrieval for global market questions. |
| LightRAG | Graph structures plus vector retrieval improve contextual awareness and efficient updates. | Use graph + vector together, with incremental updates for fast-changing market evidence. |
| RAPTOR | Recursive summaries help retrieve at different abstraction levels across long documents. | Store raw evidence plus daily/weekly/company/sector summaries for context compression. |
| HyDE | A hypothetical document can improve zero-shot dense retrieval, then real documents ground it. | Use query generation for search/retrieval, but verify against actual evidence. |
| Hybrid retrieval | Finance needs exact identifiers and relationships, not just semantic similarity. | Use BM25 + vector + graph + reranking, not vector-only RAG. |

Key links:

- GraphRAG paper: https://arxiv.org/abs/2404.16130
- Microsoft GraphRAG project: https://www.microsoft.com/en-us/research/project/graphrag/
- GraphRAG dynamic community selection: https://www.microsoft.com/en-us/research/blog/graphrag-improving-global-search-via-dynamic-community-selection/
- LightRAG: https://arxiv.org/abs/2410.05779
- RAPTOR: https://arxiv.org/abs/2401.18059
- HyDE: https://arxiv.org/abs/2212.10496

## 4. Token Optimization Research

| Research / Technique | What It Says | HIVEMIND Decision |
|---|---|---|
| LLMLingua | Prompt compression can reduce prompt tokens substantially with limited performance loss. | Add context compression before expensive model calls. |
| LongLLMLingua | Long-context prompts can be compressed and reordered to improve long-context use. | Compress retrieved bundles and put query-relevant evidence first. |
| Model routing/cascades | Cheaper models can handle many easy calls, stronger models handle hard calls. | Use Qwen/DeepSeek Flash for bulk work and reserve stronger models for final reasoning. |
| Prompt caching | Repeated context can become much cheaper where providers support cache hits. | Cache stable company, sector, source, and agent instruction packs. |
| Structured outputs | Schema-constrained JSON reduces downstream ambiguity. | Every agent output is schema validated and evidence cited. |

Key links:

- LLMLingua: https://arxiv.org/abs/2310.05736
- LongLLMLingua: https://arxiv.org/abs/2310.06839
- Microsoft LLMLingua project: https://www.microsoft.com/en-us/research/project/llmlingua/longllmlingua/

## 5. Quant And Finance Research

| Technique | Use In HIVEMIND |
|---|---|
| Event studies | Measure abnormal returns before/after order wins, results, index changes, policy events, and shocks. |
| Cross-asset event studies | Measure equity returns, yield/spread moves, commodity/FX path, and hedge performance around events. |
| Factor context | Separate issuer-specific catalyst from size, value, momentum, quality, liquidity, credit, and broad regime effects. |
| Peer-relative returns | Distinguish issuer-specific move from sector, rate, commodity, or FX rotation. |
| Regime filters | Avoid treating broad risk-on rallies as unique company events. |
| Meta-labeling | Situation engines create candidates; quant filters learn which candidates deserve attention. |
| Walk-forward validation | Train thresholds on one period and test on the next to reduce leakage and overfit. |
| Backtest-overfitting controls | Track turnover, costs, drawdown, payoff distribution, and deflated Sharpe where relevant. |
| Post-mortems | Label false positives, late alerts, early alerts, and missed catalysts. |

Key links:

- MacKinlay event studies: https://www.bu.edu/econ/files/2011/01/MacKinlay-1996-Event-Studies-in-Economics-and-Finance.pdf
- Fama/French factors: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
- Carhart momentum factor: https://ideas.repec.org/a/bla/jfinan/v52y1997i1p57-82.html
- Lopez de Prado meta-labeling concepts: https://www.cambridge.org/core/books/advances-in-financial-machine-learning/5C0AEAC9DD1F6D968B7B9B27D2F4F5EE
- Deflated Sharpe ratio / backtest overfitting: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551
- QuantConnect LEAN event-driven backtesting engine: https://github.com/QuantConnect/Lean
- vectorbt backtesting project: https://vectorbt.dev/

## 6. Market Data Findings

### Official Sources

| Source | Finding | Decision |
|---|---|---|
| NSE real-time data | NSE says real-time data is provided across levels and segments including CM, F&O, currency derivatives, WDM. | Official exchange data is the long-term truth path. |
| BSE market data products | BSE offers real-time, EOD, historical, corporate data and lists vendors. | Use BSE for announcements/corporate data and vendor discovery. |
| MCX datafeed | MCX offers real-time, delayed, EOD, and historical datafeed categories. | MCX is needed for commodity/metals lane. |
| CCIL | CCIL publishes bond and money-market data/statistics. | Use for bond/rate context. |
| SEBI RSS | SEBI exposes latest press releases, circulars, orders/rulings via RSS. | Ingest as regulatory event lane. |
| PIB RSS | PIB provides RSS feeds for official government releases. | Ingest policy and ministry events. |
| MoSPI/eSankhyiki | MoSPI provides official statistics and a Python library/API workflow. | Use for CPI, IIP, GDP, WPI, employment, energy, and macro features. |
| RBI DBIE | RBI Database on Indian Economy hosts macro and financial time series. | Use for rates, liquidity, credit, inflation, FX, and banking context. |

### Paid / Broker Sources

| Source | Finding | Decision |
|---|---|---|
| TrueData | Market Data API page says authorized NSE, BSE, MCX API coverage; pricing depends on exchange/symbol/data type and exchange fees may be separate. Public Velocity pricing lists Rs 1,439.83 to Rs 2,795.83/month per segment, but Market Data API subscription should be quoted directly. | Best serious-beta candidate to quote for authorized coverage. Do not treat Velocity pricing as final raw API licensing. |
| Global Datafeeds | Site says authorized realtime L1 vendor for NSE, MCX, BSE, NCDEX and fundamental data. | Strong candidate for broad authorized feed; get quote/API details. |
| Accelpix | Public pricing lists Smart Rs 1,355/month, Pro Rs 2,118/month, and Ultimate Rs 2,965/month + GST, with current-day tick, 1-minute history, EOD history, and symbol-at-a-time limits varying by plan. API page notes subscriber charting/analysis licensing. | Good price-to-result for personal/research workflows; verify limits/legal use. |
| DhanHQ | Official support lists Rs 499 + taxes/month for live market feed, quotes, historical, intraday. | Good MVP live feed candidate. |
| Zerodha Kite | Official support lists Connect at Rs 500/month with WebSocket real-time and historical candles. | Good MVP auxiliary feed and benchmark. |
| NSE direct data | NSE domestic pricing effective April 1, 2026 lists examples such as CM EOD Rs 1,00,000/year, CM historical trade data Rs 1,10,000/year, and CM L1 internal display Rs 24,40,000/year. | Use this to show investors when market-data costs become serious; BSE/MCX and redistribution rights are separate. |
| FYERS, Angel SmartAPI, ICICI Breeze | Official pages describe free APIs with live/historical market data features. | Useful auxiliary feeds; must reconcile quality and limits. |

### Historical Data Findings

| Source | Historical Coverage Signal | HIVEMIND Decision |
|---|---|---|
| DhanHQ | Official docs say daily historical OHLCV is available back to stock inception; intraday historical data is available for the last 5 years in 1/5/15/25/60 minute intervals, with 90-day request chunks. | Strong low-cost historical/live MVP lane; store our own local copy for replay. |
| Zerodha Kite Connect | Official product page says Connect includes historical candle data for Rs 500/month; historical docs describe minute, 3-minute, 5-minute, hourly, and daily candles across exchanges. | Useful benchmark and auxiliary historical feed. |
| FYERS | Official support says Trading API is free and includes historical data, quotes, and market data. | Add as a free cross-check source, then test quality and rate limits. |
| ICICI Breeze | Official page says customers can use Breeze API and create apps free of charges; it advertises historical data and streaming OHLC. | Useful free auxiliary source, especially if account setup is easy. |
| Angel SmartAPI | Official FAQ says SmartAPI is free, including historical data, and supports all segments. | Useful free auxiliary source; test reliability and schema stability. |
| Accelpix | Pricing page includes EOD history, 1-minute history, and tick-history depth by plan. | Good retail-priced historical feed for research/backfill pilots. |
| BSE | Market data products page says BSE has historical trading and corporate data, with segment-wise daily price/volume data since 1990. | Important for BSE-exclusive names and long-run backfills. |
| NSE direct | Domestic pricing file separates EOD/reference and historical data products. | Use direct licensing only after beta proves demand and compliance scope. |

Conclusion:

```text
Historical data is the training ground and audit layer.
Live data tells us what is happening now.
Historical data tells us whether the system is useful, early, late, or noisy.
Free official data is enough for the first evidence-and-situation prototype.
Broker APIs are cheap for MVP live and historical auxiliary signals.
An authorized vendor is the right next step if the promise is "capital-markets data across shares, debt, commodities, FX, derivatives, full historical replay, and reliable coverage."
```

## 7. Model Pricing Findings

As of the current research pass:

| Provider/Model | Official Price Signal | Design Decision |
|---|---|---|
| Qwen3.5-Flash | Alibaba Cloud lists global minimum pricing around $0.029/M input and $0.287/M output; US Qwen-Flash shows $0.05/M input and $0.40/M output. | Bulk extraction/classification/query generation can be extremely cheap. |
| DeepSeek V4 Flash | Official page lists $0.14/M cache-miss input, $0.0028/M cache-hit input, and $0.28/M output. | Strong default for cheap synthesis and many agents. |
| DeepSeek V4 Pro | Official page lists $0.435/M cache-miss input and $0.87/M output under the current pricing structure. | Reserve for final/high-value reasoning. |

Example costs:

| Task | Assumption | Approx Cost |
|---|---|---|
| Cheap extraction | 4k input + 0.8k output | about $0.00035 on Qwen Flash or $0.00078 on DeepSeek Flash |
| Deep review | 12k input + 1.5k output | about $0.0021 on DeepSeek Flash or $0.0065 on DeepSeek Pro |
| Final brief | 25k input + 2.5k output | about $0.013 on DeepSeek Pro uncached |

Key links:

- DeepSeek pricing: https://api-docs.deepseek.com/quick_start/pricing
- Alibaba Cloud Model Studio/Qwen pricing: https://www.alibabacloud.com/help/en/model-studio/models

## 8. Adopted Design Decisions

| Research Insight | HIVEMIND Decision |
|---|---|
| Swarms work best with roles and orchestration | Make AI swarms first-class across ingestion, research, quant, risk, and synthesis. |
| GraphRAG helps global sensemaking | Build issuer-sector-policy-tender-commodity-rate-credit-derivative graph memory. |
| Vector-only RAG is weak for finance | Use BM25 + vector + graph + reranking. |
| Token costs can be crushed with routing | Use model cascade, prompt caching, compression, and confidence gates. |
| Finance needs validation, not just explanation | Add event studies, cross-asset outcomes, walk-forward validation, hedge simulation, post-mortems. |
| Search is powerful but noisy | Use search as triggered discovery/audit, not truth. |
| Capital-market data is fragmented | Build source health, entity resolution, cross-asset graph links, and missed-event audit as product infrastructure. |
| Market structure matters | Add MSCI/FTSE/Nifty/BSE/F&O/surveillance/block/bulk as first-class event lanes. |
| Macro shocks transmit unevenly | Map shocks to company exposure before scoring. |
| Valuation changes interpretation | Separate catalyst detection from price paid and expectations already embedded. |
