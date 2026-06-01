# AI Learning Roadmap for Backend Developers

A practical, deep, project-driven roadmap for learning AI as a backend developer with some applied AI exposure.

This roadmap avoids books and videos by design. It favors high-quality online reading, official documentation, hands-on projects, and progress checkpoints.

---

## Guiding Principle

Learn AI from the outside in.

Do not start by trying to master every mathematical detail. Start by understanding how AI systems behave, then learn how to build with them, then learn how they work internally, then learn how to ship them safely.

```text
Concrete systems -> mental models -> implementation -> evaluation -> production judgment
```

As a backend developer, your advantage is huge. Modern AI products are not just models. They are backend systems wrapped around probabilistic components.

```text
Production AI system =
model
+ retrieval
+ tools
+ validation
+ evals
+ logging
+ permissions
+ cost controls
+ fallbacks
```

---

## Roadmap Overview

Suggested duration: 12-20 weeks

Suggested weekly effort: 6-10 hours

Main outcome: you should be able to design, build, evaluate, and deploy AI-backed backend systems.

| Level | Theme | Main Skill |
|---|---|---|
| 0 | Orientation | Understand core AI terms and system boundaries |
| 1 | Python AI Toolkit | Work with data, notebooks, APIs, and experiments |
| 2 | Classical Machine Learning | Understand prediction, features, and evaluation |
| 3 | Deep Learning and Transformers | Understand tokens, embeddings, attention, and inference |
| 4 | LLM Application Development | Build reliable AI features using model APIs |
| 5 | Embeddings and RAG | Build document/search/chat systems over private data |
| 6 | Tool Calling and Agents | Let models safely call backend functions |
| 7 | Evaluation | Measure quality instead of guessing |
| 8 | Production AI Engineering | Ship AI systems with cost, latency, safety, and observability |
| 9 | Fine-Tuning and Open Models | Know when and how to customize models |

---

# Level 0: Orientation

## Goal

Build a mental map of AI so every future topic has a place.

## Core Concepts

| Term | Backend-Friendly Meaning |
|---|---|
| AI | Broad category: software that performs tasks requiring intelligence |
| ML | Systems that learn patterns from data |
| Deep Learning | ML using neural networks |
| LLM | A deep learning model trained to predict and generate language |
| Embedding | A numerical representation of meaning |
| RAG | Retrieval-Augmented Generation: fetch relevant data, then ask the LLM to answer |
| Agent | LLM plus tools, memory, planning, or multi-step execution |
| Fine-tuning | Further training a model on examples |
| Inference | Running the trained model |
| Training | Updating model weights using data |

## Learn

- Difference between deterministic software and probabilistic software
- Why LLMs hallucinate
- Why AI accuracy is not one simple metric
- How prompts, context, retrieval, tools, and evaluation fit together
- Why backend engineering matters more than fancy prompting in production

## Reading Resources

- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course)
- [OpenAI Model Selection Guide](https://platform.openai.com/docs/guides/model-selection)
- [Hugging Face Course: Introduction](https://huggingface.co/course/chapter1)

## Completion Checkpoint

You should be able to explain this without notes:

```text
A user asks a question.
The backend retrieves relevant documents.
The LLM receives the question plus retrieved context.
The LLM generates an answer.
The system validates, logs, and returns the result.
```

You are ready for the next level when you can also explain how this flow can fail.

## Tracker

- I can explain AI vs ML vs deep learning vs LLMs
- I can explain training vs inference
- I can explain why LLMs hallucinate
- I can explain what embeddings are
- I can explain the high-level RAG flow

---

# Level 1: Python AI Toolkit

## Goal

Become comfortable enough with Python AI tooling to build experiments and services.

As a backend developer, you do not need to become a full data scientist first. But you do need enough Python to manipulate data, call models, run notebooks, and build APIs.

## Learn

| Topic | What You Need |
|---|---|
| Python environments | venv, pip, dependency isolation, .env files |
| Notebooks | Fast experimentation and inspecting intermediate outputs |
| NumPy | Arrays, vector operations, shapes |
| pandas | CSVs, data cleaning, grouping, missing values |
| Matplotlib | Basic charts and data visualization |
| API backend | FastAPI or your preferred backend stack |
| Experiment hygiene | Save inputs, outputs, configs, and metrics |

## Project: CSV Profiler API

Build a tiny dataset inspector.

Input:

```text
CSV file
```

Output:

```text
- row count
- missing values
- column types
- simple charts
- train/test split preview
```

Suggested endpoints:

```http
POST /datasets/upload
GET /datasets/{id}/profile
```

## Reading Resources

- [pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html)
- [NumPy Absolute Beginners Guide](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [Matplotlib Quick Start](https://matplotlib.org/stable/users/explain/quick_start.html)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

## Completion Checkpoint

You can load a CSV, clean simple columns, split data into train/test sets, and expose the result through an API.

## Tracker

- I can create and use a Python virtual environment
- I can load CSV data with pandas
- I can inspect missing values and column types
- I can create basic charts
- I can expose a simple FastAPI endpoint
- I completed the CSV Profiler API

---

# Level 2: Classical Machine Learning

## Goal

Understand prediction systems before jumping deep into LLMs.

This matters because production AI still uses many classical ML ideas: features, labels, evaluation, overfitting, precision, recall, and error analysis.

## Mental Model

```text
historical data -> features -> model -> prediction -> evaluation
```

Example:

```text
support ticket text + customer plan + account age
-> model
-> billing, bug, feature request, urgent
```

## Learn

| Topic | Question You Should Be Able To Answer |
|---|---|
| Supervised learning | What are labels and training examples? |
| Classification | How do we predict categories? |
| Regression | How do we predict numbers? |
| Train/test split | Why not evaluate on training data? |
| Overfitting | Why does a model memorize instead of generalize? |
| Precision/recall | Which mistakes are expensive? |
| Confusion matrix | Where exactly is the model failing? |
| Feature engineering | How do raw inputs become model inputs? |
| Baselines | What simple model must we beat? |

## Project: Support Ticket Classifier

Build a classifier.

Input:

```text
My card was charged twice this month
```

Output:

```json
{
  "category": "billing",
  "confidence": 0.86
}
```

Suggested endpoints:

```http
POST /tickets/classify
GET /models/ticket-classifier/metrics
GET /models/ticket-classifier/confusion-matrix
```

## Reading Resources

- [scikit-learn Getting Started](https://scikit-learn.org/stable/getting_started.html)
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [Google ML Crash Course: Classification](https://developers.google.com/machine-learning/crash-course/classification)
- [Google ML Crash Course: Overfitting](https://developers.google.com/machine-learning/crash-course/overfitting)

## Completion Checkpoint

You can answer this:

```text
Why can a model with 95% accuracy still be bad?
```

Expected reasoning: because class imbalance, false positives, false negatives, and business cost matter.

## Tracker

- I understand supervised learning
- I understand classification vs regression
- I can split data into train and test sets
- I can explain overfitting
- I can read a confusion matrix
- I can calculate precision and recall
- I completed the Support Ticket Classifier

---

# Level 3: Deep Learning and Transformers

## Goal

Understand LLMs conceptually without getting trapped in math.

You do not need to train a transformer from scratch. You do need to understand what tokens, attention, context windows, embeddings, and inference mean.

## Learn

| Topic | Backend-Friendly Understanding |
|---|---|
| Tokenization | Text is split into model-readable pieces |
| Context window | Maximum input/output working memory |
| Embeddings | Meaning represented as vectors |
| Neural network | Function approximator with learned parameters |
| Transformer | Architecture good at modeling token relationships |
| Attention | Mechanism for relating tokens to other tokens |
| Pretraining | Model learns general language patterns |
| Instruction tuning | Model learns to follow instructions |
| Inference | Running the model to generate output |
| Temperature | Randomness control during generation |

## Project: Token and Embedding Explorer

Part 1: tokenizer explorer.

Input:

```text
Refund my payment please
```

Output:

```text
- tokens
- token count
- estimated cost for selected model
```

Part 2: embedding similarity matrix.

Input:

```text
cat, dog, invoice, payment, refund
```

Output:

```text
similarity matrix
```

## Reading Resources

- [Hugging Face Course](https://huggingface.co/course/chapter1)
- [Hugging Face Transformers Docs](https://huggingface.co/docs/transformers/index)
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [OpenAI Tokenizer](https://platform.openai.com/tokenizer)

## Completion Checkpoint

You can explain this:

```text
An LLM does not search a database by default.
It predicts likely next tokens based on its training and the context you provide.
```

## Tracker

- I understand tokenization
- I understand context windows
- I understand embeddings conceptually
- I understand what attention does at a high level
- I understand temperature and randomness
- I completed the Token and Embedding Explorer

---

# Level 4: LLM Application Development

## Goal

Learn to build useful AI features with model APIs.

This is probably the highest ROI zone for a backend developer.

## Mental Model

```text
request
-> validate input
-> construct prompt/messages
-> call model
-> parse response
-> validate output
-> store trace
-> return API response
```

## Learn

| Topic | What To Learn |
|---|---|
| Prompt structure | system, developer, user, context, output format |
| Structured outputs | JSON schemas, validation, retries |
| Streaming | Token-by-token responses |
| Tool/function calling | Model chooses backend functions |
| Model selection | Accuracy first, cost/latency second |
| Retries | Handling malformed output or transient failures |
| Prompt versioning | Treat prompts like code |
| Safety | Refusals, policy constraints, input filtering |

## Project: AI Intent Extraction API

Input:

```text
Hi, I want to cancel order #A123 because it arrived broken.
```

Output:

```json
{
  "intent": "cancel_order",
  "order_id": "A123",
  "reason": "arrived broken",
  "urgency": "normal"
}
```

Suggested endpoints:

```http
POST /ai/extract-intent
POST /ai/summarize-ticket
POST /ai/draft-reply
```

## Reading Resources

- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [OpenAI Structured Outputs Guide](https://platform.openai.com/docs/guides/structured-outputs)
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [Anthropic Prompt Engineering Docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)

## Completion Checkpoint

You can build an endpoint where the LLM reliably returns validated JSON and your backend rejects invalid output.

## Tracker

- I can structure system and user prompts
- I can request structured JSON output
- I can validate model output against a schema
- I can retry or fail gracefully when output is invalid
- I understand streaming responses
- I completed the AI Intent Extraction API

---

# Level 5: Embeddings, Semantic Search, and RAG

## Goal

Build AI systems that answer using private or fresh data.

This is one of the most important practical AI engineering skills.

## Mental Model

Indexing pipeline:

```text
documents
-> parse
-> clean
-> chunk
-> embed
-> store vectors + metadata
```

Query pipeline:

```text
question
-> embed question
-> retrieve relevant chunks
-> optionally rerank
-> send chunks to LLM
-> answer with citations
```

## Learn

| Topic | What To Learn |
|---|---|
| Document parsing | PDFs, HTML, markdown, docs, emails |
| Chunking | Split documents into answerable units |
| Embeddings | Convert chunks and queries into vectors |
| Vector DB | Store and search embeddings |
| Metadata filtering | Filter by user, organization, date, document type |
| Hybrid search | Combine keyword and vector search |
| Reranking | Improve top results before generation |
| Citations | Return source chunks used |
| Grounding | Force answers to stay inside retrieved context |
| Failure modes | Bad chunking, missing metadata, stale indexes |

## Project: Document Q&A Backend

Suggested endpoints:

```http
POST /documents/upload
POST /documents/index
POST /chat/ask
GET /chat/{id}/citations
```

Example response:

```json
{
  "answer": "The refund window is 30 days after delivery.",
  "citations": [
    {
      "document": "refund_policy.pdf",
      "page": 2,
      "chunk_id": "refund_policy_002"
    }
  ]
}
```

## Reading Resources

- [OpenAI Retrieval Guide](https://platform.openai.com/docs/guides/retrieval)
- [OpenAI Help: K-nearest embedding search](https://help.openai.com/en/articles/8984342-how-can-i-retrieve-k-nearest-embedding-vectors-quickly)
- [Pinecone RAG Guide](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- [Pinecone Chunking Strategies](https://www.pinecone.io/learn/chunking-strategies/)
- [pgvector GitHub Docs](https://github.com/pgvector/pgvector)
- [LlamaIndex RAG Introduction](https://docs.llamaindex.ai/en/stable/understanding/rag/)
- [LangChain RAG Tutorial](https://docs.langchain.com/oss/python/langchain/rag)

## Completion Checkpoint

You can explain why this is wrong:

```text
Just paste all company docs into the prompt.
```

Expected reasoning: context limits, cost, noise, irrelevant data, access control, update problems, and poor citations.

## Tracker

- I understand document parsing concerns
- I understand chunking tradeoffs
- I can generate embeddings
- I can store vectors with metadata
- I can retrieve relevant chunks
- I can produce cited answers
- I completed the Document Q&A Backend

---

# Level 6: Tool Calling and Agents

## Goal

Let AI interact with backend systems safely.

This is where backend experience becomes extremely valuable.

## Mental Model

The model should not directly do things. It should propose a tool call. Your backend validates and executes.

```text
User: Cancel my order A123
LLM: call cancel_order(order_id="A123")
Backend:
- checks auth
- checks order state
- performs cancellation
- returns result
LLM:
- explains result to user
```

## Learn

| Topic | What To Learn |
|---|---|
| Function schemas | Define tools clearly |
| Tool authorization | User can only call allowed tools |
| Idempotency | Avoid duplicate destructive actions |
| Human confirmation | Required before risky operations |
| Tool result formatting | Return compact, structured data |
| Planning | Multi-step workflows |
| Agent loops | Observe, think, act, observe |
| Sandboxing | Never let the model execute arbitrary code |
| Audit logs | Record every tool call |

## Project: AI Customer Support Agent

Tools:

```text
get_order(order_id)
cancel_order(order_id)
create_refund(order_id, reason)
create_support_ticket(user_id, summary)
```

Safety rules:

```text
- Cannot refund without order ownership check
- Cannot cancel shipped orders
- Must ask confirmation before refund
- Must log every tool call
```

## Reading Resources

- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [Hugging Face Agents Course: Function Calling](https://huggingface.co/learn/agents-course/en/bonus-unit1/what-is-function-calling)
- [LangChain RAG Agent Tutorial](https://docs.langchain.com/oss/python/langchain/rag)

## Completion Checkpoint

You can design an AI agent where the LLM is never trusted as the authority. Your backend remains the authority.

## Tracker

- I can define tool schemas
- I understand tool authorization
- I can require confirmation for risky actions
- I can design idempotent tool execution
- I can log tool calls
- I completed the AI Customer Support Agent

---

# Level 7: Evaluation

## Goal

Stop guessing whether the AI is good.

AI development without evals is like backend development without tests.

## Mental Model

A useful eval example looks like this:

```json
{
  "input": "Can I get refund after 45 days?",
  "expected_behavior": "Say no if policy says 30 days, cite refund policy.",
  "must_include": ["30 days"],
  "must_not_include": ["yes", "guaranteed"],
  "source_doc": "refund_policy.pdf"
}
```

## Evaluation Types

| Type | Used For |
|---|---|
| Exact match | Structured outputs |
| Schema validation | JSON responses |
| Human review | High-risk qualitative tasks |
| LLM-as-judge | Scoring style, helpfulness, factuality |
| Retrieval precision | Did we retrieve the right chunks? |
| Retrieval recall | Did we miss important chunks? |
| Faithfulness | Did the answer stay grounded in context? |
| Regression evals | Did a prompt/model change break behavior? |
| Latency/cost evals | Is it production-feasible? |

## Project: RAG Evaluation Suite

Create an eval suite for your RAG app:

```text
50 questions
expected answer notes
expected source document
expected citation
forbidden claims
```

Track metrics:

```text
- answer correctness
- citation correctness
- retrieval hit rate
- hallucination rate
- average latency
- average cost
```

## Reading Resources

- [OpenAI Evals GitHub](https://github.com/openai/evals)
- [Ragas Metrics Docs](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/)
- [Promptfoo Docs](https://www.promptfoo.dev/docs/intro/)
- [Promptfoo Eval Guides](https://www.promptfoo.dev/docs/guides/)
- [LangSmith RAG Evaluation Tutorial](https://docs.langchain.com/langsmith/evaluate-rag-tutorial)

## Completion Checkpoint

Before changing your prompt, model, chunking, or retriever, you can run an eval and compare before/after.

## Tracker

- I can create an eval dataset
- I can validate structured outputs
- I can evaluate retrieval quality
- I can evaluate groundedness or faithfulness
- I can compare prompt/model versions
- I completed the RAG Evaluation Suite

---

# Level 8: Production AI Engineering

## Goal

Ship AI-backed systems that behave well under real users.

## Learn

| Concern | What To Design |
|---|---|
| Latency | Streaming, async jobs, p95 tracking |
| Cost | Token limits, caching, model routing |
| Reliability | Retries, fallbacks, circuit breakers |
| Observability | Traces, prompts, model responses, tool calls |
| Security | Prompt injection, data exfiltration, auth |
| Privacy | PII redaction, retention, tenant isolation |
| Versioning | Prompt version, model version, embedding version |
| Access control | Document-level permissions in RAG |
| Abuse handling | Rate limits, quotas, moderation |
| Rollbacks | Revert prompt/model/retriever changes |

## Reference Architecture

```text
API Gateway
-> Auth
-> AI Orchestrator Service
-> Prompt Registry
-> Model Provider Client
-> Retrieval Service
-> Tool Execution Service
-> Eval Service
-> Trace/Logging Store
-> Cost Metering
```

## Project: Production AI Knowledge Assistant

Upgrade your document Q&A app into a production-style service.

Features:

```text
- user auth
- per-user documents
- document permissions
- background indexing job
- streaming answers
- citations
- eval dashboard
- token/cost logging
- prompt versioning
- fallback model
```

## Reading Resources

- [OpenAI Production Best Practices](https://platform.openai.com/docs/guides/production-best-practices)
- [OpenAI Model Selection Guide](https://platform.openai.com/docs/guides/model-selection)
- [Promptfoo Red Teaming Docs](https://www.promptfoo.dev/docs/red-team/)
- [LangChain RAG Security Note](https://docs.langchain.com/oss/python/langchain/rag)

## Completion Checkpoint

You can answer these design questions:

```text
What happens if the model times out?
What happens if retrieved context contains malicious instructions?
What happens if the answer has no supporting source?
What happens if cost spikes 10x?
What happens if a user asks about another user's document?
```

## Tracker

- I can design retries and fallbacks
- I can track token usage and cost
- I can stream model responses
- I can version prompts
- I can protect against basic prompt injection
- I can enforce document permissions
- I completed the Production AI Knowledge Assistant

---

# Level 9: Fine-Tuning and Open Models

## Goal

Understand when model customization is worth it.

Most beginners reach for fine-tuning too early. Usually the better order is:

```text
better prompt
-> better examples
-> structured output
-> better retrieval
-> better evals
-> model switch
-> fine-tuning
```

## When Fine-Tuning Helps

| Good Use Case | Bad Use Case |
|---|---|
| Consistent style | Teaching private knowledge |
| Classification | Replacing a database |
| Structured behavior | Fixing bad retrieval |
| Domain-specific phrasing | Making model remember docs |
| Tool-call format improvement | Avoiding evals |

## Learn

- Supervised fine-tuning
- Dataset preparation
- Train/validation splits
- Evaluation before and after tuning
- LoRA and PEFT
- Open-source model serving basics
- Quantization basics
- GPU cost tradeoffs

## Reading Resources

- [OpenAI Supervised Fine-Tuning Guide](https://platform.openai.com/docs/guides/supervised-fine-tuning)
- [OpenAI Fine-Tuning Help Center](https://help.openai.com/en/collections/6864540-fine-tuning)
- [Hugging Face Fine-Tuning Guide](https://huggingface.co/docs/transformers/training)
- [Hugging Face PEFT LoRA Docs](https://huggingface.co/docs/peft/v0.18.0.rc0/en/package_reference/lora)

## Completion Checkpoint

You can explain why RAG is usually better than fine-tuning for private knowledge.

Expected reasoning: RAG is easier to update, cite, permission, debug, and evaluate.

## Tracker

- I know when not to fine-tune
- I understand fine-tuning vs RAG
- I can prepare a small fine-tuning dataset
- I understand LoRA at a high level
- I understand open-model serving tradeoffs

---

# 16-Week Progress Plan

## Weeks 1-2: Orientation and Python AI Basics

- Read AI/ML/LLM terminology resources
- Set up Python AI environment
- Learn basic pandas, NumPy, and notebooks
- Build CSV Profiler API
- Explain training vs inference

## Weeks 3-4: Classical ML

- Learn classification and regression
- Learn train/test split and overfitting
- Learn precision, recall, and F1
- Build ticket classifier
- Expose model metrics through API

## Weeks 5-6: LLM API Basics

- Learn prompt structure
- Learn structured outputs
- Learn streaming
- Build intent extraction endpoint
- Add schema validation and retries

## Weeks 7-9: Embeddings and RAG

- Learn embeddings
- Learn chunking
- Learn vector search
- Build document ingestion pipeline
- Build Q&A endpoint with citations
- Add metadata filters

## Weeks 10-11: Tool Calling and Agents

- Learn function/tool calling
- Design safe tool schemas
- Build support agent with backend tools
- Add confirmation for risky actions
- Log all tool calls

## Weeks 12-13: Evaluation

- Create 50-question eval dataset
- Add schema evals
- Add retrieval evals
- Add answer quality evals
- Compare two prompts/models

## Weeks 14-15: Production Hardening

- Add token/cost logging
- Add streaming responses
- Add rate limits
- Add prompt versioning
- Add prompt injection defenses
- Add fallback behavior

## Week 16: Capstone

Build an AI Knowledge Assistant Backend.

Features:

- Upload documents
- Background indexing
- Ask questions
- Cite sources
- Stream answers
- Use tool calling for backend actions
- Evaluate answers
- Track cost and latency
- Dockerized API

---

# Project Sequence

Build these in order.

| Project | Why It Matters |
|---|---|
| CSV Profiler API | Gets you comfortable with data workflows |
| Ticket Classifier | Teaches classical ML and evaluation |
| Intent Extractor | Teaches structured LLM outputs |
| Document Q&A API | Teaches embeddings and RAG |
| Support Agent | Teaches tool calling and safety |
| Eval Harness | Teaches test-driven AI development |
| Production AI Backend | Combines everything |

---

# Things To Avoid Early

| Avoid | Reason |
|---|---|
| Starting with heavy math | Slows you down before you have intuition |
| Starting with fine-tuning | Usually the wrong first solution |
| Watching random AI influencer content | Too shallow and noisy |
| Building only chatbots | You miss extraction, retrieval, evals, and tools |
| Trusting demos | AI demos hide failure cases |
| Ignoring evals | You will not know whether you improved anything |
| Overusing frameworks early | Learn the raw workflow before hiding it behind abstractions |

---

# North-Star Mental Model

```text
AI model = unreliable probabilistic engine

Production AI system =
model
+ retrieval
+ tools
+ validation
+ evals
+ logging
+ permissions
+ cost controls
+ fallbacks
```

Your backend skill is not secondary. It is the thing that makes AI usable.

---

# Final Master Checklist

## Fundamentals

- I understand AI, ML, deep learning, and LLMs
- I understand training vs inference
- I understand tokenization
- I understand embeddings
- I understand transformers at a high level

## Backend AI Application Development

- I can call an LLM API safely
- I can create structured outputs
- I can validate model responses
- I can stream responses
- I can version prompts

## RAG

- I can parse documents
- I can chunk documents
- I can create embeddings
- I can store vectors
- I can retrieve relevant chunks
- I can answer with citations
- I can enforce document permissions

## Agents and Tools

- I can define backend tools for an LLM
- I can validate tool calls
- I can require confirmation for risky actions
- I can log tool execution
- I can prevent the model from becoming the authority

## Evaluation and Production

- I can create eval datasets
- I can compare model/prompt versions
- I can measure hallucination and citation correctness
- I can track cost and latency
- I can handle retries and fallbacks
- I can protect against basic prompt injection

## Advanced

- I know when fine-tuning is useful
- I know when RAG is better than fine-tuning
- I understand LoRA at a high level
- I understand open-source model serving tradeoffs
