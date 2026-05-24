# AI Agent Developer Knowledge Base

## Core Concepts

### Prompt Engineering
- System prompts, user prompts, and assistant prompts
- Chain-of-thought and structured output prompts
- Few-shot and zero-shot prompt patterns
- Prompt templates and dynamic context injection

### Tools
- Tool specs and tool calling patterns
- Tool verification and safe execution
- API connectors for search, databases, and actions
- Tool orchestration and fallback handling

### Memory
- Working memory vs. long-term memory
- Episodic memory and session state
- Vector embeddings and semantic retrieval
- Cache, compression, and context budgeting

### RAG
- Document retrieval and ranking
- Dense embeddings + sparse search fusion
- Alignment of retrieval results with prompt context
- Retrieval quality evaluation

### Orchestration
- Single-agent vs. multi-agent pipelines
- Debate, critique, and coordinator agents
- Task decomposition and action sequencing
- Retry, rollback, and monitoring patterns

### Frameworks
- LangChain and similar orchestration libraries
- Agent frameworks and execution environments
- Prompt management tools and versioning
- Logging, telemetry, and observability for agents

### Evaluation
- Accuracy, relevance, and faithfulness
- Hallucination mitigation
- Response latency and cost metrics
- User satisfaction and task completion

## Practical Reference

### Recommended Tools
- OpenAI / Anthropic / Google Gemini APIs
- LangChain, LlamaIndex, Agentsmith, Microsoft Semantic Kernel
- Vector databases: Qdrant, Pinecone, Milvus
- Search services and knowledge base connectors

### Patterns and Templates
- Prompt template for tool-enabled agent
- Memory retrieval and context assembly
- RAG pipeline with retrieval + rerank + generation
- Orchestration flow for multi-agent decision-making

### Example Focus Areas
- Customer support chatbot with tool access
- Research agent summarizing documents
- Workflow automation agent calling APIs
- Browser agent simulation and task execution

## Study Plan

1. Learn prompt engineering basics
2. Build a single-agent app with tool calls
3. Add retrieval and memory support
4. Expand to multi-agent orchestration
5. Measure and iterate using evaluation metrics
