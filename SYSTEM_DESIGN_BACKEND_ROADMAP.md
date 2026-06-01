# System Design Roadmap for Backend Developers

A deep, practical, modern system design roadmap for backend developers.

This roadmap avoids paid sources, books, videos, and generic toy prompts like URL shorteners. It focuses on real design judgment: databases, queues, Kafka, Redis, BullMQ, fan-in/fan-out, push vs pull, CAP, consistency, scaling, failure handling, and modern backend problems.

All linked resources are free to read.

---

## Guiding Principle

System design is not about memorizing architectures.

It is about learning to ask:

```text
What are the constraints?
What must be consistent?
What can be async?
What can fail?
What is the bottleneck?
What data shape are we storing?
What access patterns matter?
What happens at 10x traffic?
What happens during partial failure?
```

A good design is not the one with the most components. A good design is the one where every component earns its place.

---

## What This Roadmap Optimizes For

You should be able to design systems like:

- notification platforms
- event-driven payment systems
- order processing pipelines
- AI document ingestion systems
- real-time collaboration backends
- analytics/event tracking platforms
- multi-tenant SaaS platforms
- workflow orchestration engines
- search and recommendation systems
- chat and presence systems
- fraud/risk pipelines
- rate-limited API platforms
- large file/video processing systems

You should also be able to explain:

- why Kafka instead of RabbitMQ
- why SQS instead of BullMQ
- why Redis is dangerous as a source of truth
- why Postgres is often the best default
- why DynamoDB needs access-pattern-first design
- why MongoDB is not just "JSON Postgres"
- what CAP actually says and what people get wrong
- how fan-out differs from competing consumers
- when push beats pull and when pull beats push
- how to handle retries without double-charging users

---

## Roadmap Overview

Suggested duration: 14-20 weeks

Suggested weekly effort: 6-10 hours

| Level | Theme | Main Skill |
|---|---|---|
| 0 | System Design Foundations | Think in requirements, bottlenecks, SLOs, and tradeoffs |
| 1 | API and Communication Patterns | Choose sync, async, streaming, polling, webhook, or event-driven flows |
| 2 | Data Modeling and Database Choice | Pick the right database based on access patterns and consistency needs |
| 3 | Consistency, CAP, and Distributed Tradeoffs | Understand failure, replication, partitions, and consistency models |
| 4 | Caching and Redis | Use Redis safely for cache, coordination, rate limits, queues, streams, and pub/sub |
| 5 | Queues and Background Jobs | Design reliable async work with retries, DLQs, idempotency, and backpressure |
| 6 | Kafka and Event Streaming | Design durable event logs, consumer groups, partitions, replay, and stream processing |
| 7 | Fan-In, Fan-Out, Push, and Pull | Design multi-consumer, broadcast, aggregation, and delivery systems |
| 8 | Sockets and Real-Time Broadcasting | Design WebSocket, SSE, rooms, presence, reconnect, and broadcast systems |
| 9 | Scaling, Partitioning, and Hotspots | Scale reads, writes, storage, and consumers without melting one key/partition |
| 10 | Reliability and Failure Handling | Design for retries, partial failure, circuit breakers, degradation, and recovery |
| 11 | Observability and Operations | Use metrics, logs, traces, alerts, dashboards, and runbooks |
| 12 | Security, Multi-Tenancy, and Compliance | Handle tenant isolation, authz, secrets, PII, and audit trails |
| 13 | Modern Design Problems | Practice real modern systems, not stale toy problems |

---

# Inductive Learning Spine

Use this roadmap problem-first.

Do not start by memorizing Kafka, Redis, CAP, sharding, and queues as isolated topics. Start from concrete backend pain, then introduce the tool because the pain demands it.

The learning sequence should feel like this:

```text
1. A real backend system starts simple.
2. A new requirement or failure appears.
3. The current design breaks or becomes awkward.
4. A system design concept solves that pressure.
5. We generalize the lesson.
6. We learn the tradeoffs and failure modes.
```

That is the whole inductive method.

---

## Problem-First Path

Follow these in order. Each problem introduces one new design pressure.

| Step | Start With This Problem | Pain You Discover | Concept You Earn |
|---|---|---|---|
| 1 | Product API with normal CRUD | slow endpoints, unclear requirements | SLOs, capacity estimates, API design |
| 2 | Checkout endpoint | too many things happen synchronously | async work, queues, idempotency |
| 3 | Webhook payment processor | duplicate and out-of-order events | idempotency keys, state machines, reconciliation |
| 4 | Notification system | one event must trigger many channels | fan-out, per-channel queues, provider isolation |
| 5 | Video/document processing | parallel jobs must join back together | fan-in, workflow state, DLQs |
| 6 | Analytics event pipeline | many consumers need the same events | Kafka, partitions, replay, consumer groups |
| 7 | Real-time collaboration | users need instant updates | WebSockets, Redis Pub/Sub, durable logs |
| 8 | Product search | SQL filters are not enough | search indexes, source-of-truth vs projection |
| 9 | Feed/ranking system | read-vs-write fan-out tradeoff appears | fan-out-on-write, fan-out-on-read, hybrid feeds |
| 10 | Multi-tenant SaaS | tenant leaks become catastrophic | authz, tenant isolation, scoped keys |
| 11 | High-scale hot tenant | one key/partition melts | partitioning, sharding, hot key mitigation |
| 12 | Regional failure | correctness and availability conflict | CAP, consistency models, graceful degradation |
| 13 | Production incident | nobody knows what broke | observability, alerts, runbooks |

Each step should produce a design note:

```text
Initial simple design:
What broke:
New requirement:
Design change:
New component added:
Why this component:
Failure modes introduced:
Operational metrics:
What I would avoid:
```

---

## Inductive Rulebook

These are the rules you should discover as you move through the problems.

### Rule 1: Start Synchronous, Then Cut Async Boundaries

Start with a direct request-response flow.

When the request starts doing slow, unreliable, or non-user-critical work, move that work behind a queue.

Example:

```text
Checkout should not wait for:
- email delivery
- analytics update
- warehouse notification
- recommendation refresh
```

General rule:

```text
Keep the user-critical transaction small.
Push side effects into durable async workflows.
```

### Rule 2: Add Queues Because Something Needs Protection

A queue is not decoration. It protects something.

It may protect:

- the user from slow work
- the database from spikes
- a third-party provider from overload
- workers from producer bursts
- the system from temporary downstream failure

If you cannot say what the queue protects, you may not need it.

### Rule 3: Add Kafka When Events Become Shared History

Use a normal queue when work has one logical consumer.

Use Kafka or another event stream when events become durable shared history.

Queue question:

```text
Who needs to do this job?
```

Kafka question:

```text
Who might need to know this happened, now or later?
```

### Rule 4: Add Redis When You Need Fast Ephemeral State

Redis is excellent for:

- cache
- sessions
- rate limits
- leaderboards
- ephemeral locks
- short-lived coordination
- BullMQ jobs
- Pub/Sub live signals

Redis is dangerous when it quietly becomes the only source of truth for critical business state.

### Rule 5: Choose Databases From Access Patterns

Do not choose a database by popularity.

Choose by answering:

```text
What are my top queries?
What must be atomic?
What must be indexed?
What grows fastest?
What can be stale?
What must be recoverable?
```

### Rule 6: Every Async System Needs Idempotency

If a job, webhook, Kafka event, or queue message can be retried, it can happen twice.

Therefore every serious async handler needs:

- stable message ID
- idempotency key
- processed-message tracking
- safe state transition
- retry policy
- DLQ or repair path

### Rule 7: Fan-Out Creates Multiplication

One event becoming many jobs multiplies:

- cost
- retries
- failures
- latency variability
- provider rate-limit problems
- observability needs

Fan-out needs isolation. Usually that means separate queues, separate rate limits, and separate DLQs per downstream concern.

### Rule 8: Fan-In Requires State

If many parallel jobs must finish before the next step, you need a state store.

You need to track:

- required steps
- completed steps
- failed steps
- timeout
- retry state
- final status

Fan-in without state becomes guesswork.

### Rule 9: Push for Freshness, Pull for Control

Push is good for low-latency notification.

Pull is good for backpressure and canonical state.

Modern real-time systems often combine them:

```text
push: "something changed"
pull: "fetch the latest truth"
```

### Rule 10: CAP Is About Failure-Time Choices

CAP is not a sticker you put on databases.

It asks:

```text
During a network partition,
will this operation reject work to preserve correctness,
or accept work and reconcile later?
```

Make that decision per operation, not vaguely per system.

---

## How To Study Each Level

For every level below, use this loop:

```text
1. Build the naive version mentally.
2. Add one painful requirement.
3. Watch the naive version break.
4. Introduce the design concept.
5. Draw the new flow.
6. List new failure modes.
7. Add metrics and recovery paths.
```

Example:

```text
Naive: send notification inside request.
Pain: email provider is slow.
Break: API latency spikes.
Concept: queue.
New flow: API writes notification job, worker sends email.
New failures: duplicate jobs, provider failure, poison message.
Recovery: idempotency key, retries, DLQ.
Metrics: queue depth, oldest job age, provider error rate.
```

This is how the rest of the document should be read.

---

# Level 0: System Design Foundations

## Goal

Build the language of system design.

Before choosing Kafka, Redis, Postgres, or DynamoDB, you need to understand the shape of the problem.

## Core Concepts

| Concept | Practical Meaning |
|---|---|
| Functional requirements | What the system must do |
| Non-functional requirements | Latency, availability, durability, scale, security, cost |
| SLO | Target behavior, such as 99.9% successful requests under 300ms |
| SLA | Contractual promise, usually with penalties |
| Throughput | Work per unit time, such as requests/sec or messages/sec |
| Latency | Time taken for one request or job |
| p95/p99 | Tail latency, where real user pain often lives |
| Bottleneck | The limiting resource: CPU, DB, network, disk, lock, partition, queue |
| Backpressure | Slowing producers when consumers cannot keep up |
| Load shedding | Dropping or rejecting work to protect the system |
| Idempotency | Same operation can be safely retried |
| Durability | Data survives crashes |
| Availability | System continues serving requests |
| Consistency | Users see correct and expected data |

## The System Design Flow

Use this order:

```text
1. Clarify requirements
2. Define scale assumptions
3. Identify core entities
4. Define APIs and access patterns
5. Choose data stores
6. Choose sync vs async boundaries
7. Design critical flows
8. Handle failures
9. Scale bottlenecks
10. Add observability, security, and operations
```

## Capacity Estimation Template

For every design, estimate:

```text
Daily active users:
Peak requests per second:
Average payload size:
Read/write ratio:
Storage growth per day:
Retention period:
Hot entities:
Fan-out multiplier:
Expected queue backlog:
Required p95 latency:
Required durability:
```

## Example

If 1 million users each generate 20 events/day:

```text
20 million events/day
~231 events/sec average
Maybe 10x peak = 2,310 events/sec
Payload 2 KB = ~40 GB/day raw
Retention 90 days = ~3.6 TB raw before indexes/replication
```

That immediately affects database, queue, storage, and partition choices.

## Reading Resources

- [Google SRE Book: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/)
- [Google SRE Book: Handling Overload](https://sre.google/sre-book/handling-overload/)
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)

## Tracker

- [ ] I can separate functional and non-functional requirements
- [ ] I can estimate QPS, storage, and fan-out
- [ ] I understand p95 and p99 latency
- [ ] I understand bottlenecks and backpressure
- [ ] I can explain idempotency

---

# Level 1: API and Communication Patterns

## Goal

Choose the right communication model instead of defaulting to REST for everything.

## Communication Options

| Pattern | Best For | Weakness |
|---|---|---|
| REST | Resource CRUD, public APIs, simple integrations | Can become chatty |
| gRPC | Internal service-to-service APIs, low latency, typed contracts | Less browser/native-public friendly |
| GraphQL | Client-driven reads, complex frontend data needs | Can hide expensive queries |
| WebSocket | Real-time bidirectional updates | Connection state and scaling complexity |
| Server-Sent Events | Server-to-client streaming | One-way only |
| Webhook | Third-party async notification | Retries and signature verification required |
| Polling | Simple client refresh | Wasteful at scale |
| Long polling | Near-real-time without WebSockets | More server state than simple polling |
| Message queue | Async background work | Requires idempotency and retry design |
| Event stream | Durable ordered event history | Requires partition and consumer design |

## Sync vs Async Decision

Use synchronous calls when:

- user needs immediate answer
- dependency is fast and reliable
- failure can be shown to user immediately
- transaction boundary is small

Use asynchronous flow when:

- work is slow
- work can retry later
- downstream systems are unstable
- fan-out is needed
- user does not need final result immediately
- spike absorption matters

## Example: Checkout Flow

Bad design:

```text
POST /checkout
-> charge card
-> update inventory
-> send email
-> notify warehouse
-> update analytics
-> return response after all finish
```

Better design:

```text
POST /checkout
-> validate cart
-> create order
-> reserve inventory
-> charge payment
-> commit order
-> publish OrderCreated event
-> return response

Async consumers:
-> send email
-> notify warehouse
-> update analytics
-> start fraud review
```

## API Design Checklist

- [ ] Is the operation idempotent?
- [ ] Does the client provide an idempotency key?
- [ ] What is the timeout?
- [ ] What happens if the client retries?
- [ ] Are errors retryable or permanent?
- [ ] Are pagination and filtering bounded?
- [ ] Are bulk endpoints needed?
- [ ] Are webhook retries safe?
- [ ] Is the API versioned?

## Reading Resources

- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)
- [Google API Improvement Proposals](https://google.aip.dev/)
- [gRPC Concepts](https://grpc.io/docs/what-is-grpc/core-concepts/)
- [MDN WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
- [MDN Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)

## Tracker

- [ ] I can choose sync vs async communication
- [ ] I understand REST, gRPC, WebSockets, SSE, webhooks, queues, and streams
- [ ] I can design idempotent APIs
- [ ] I can define retry-safe error behavior

---

# Level 2: Data Modeling and Database Choice

## Goal

Choose databases based on data shape, access patterns, consistency needs, and operational constraints.

## First Principle

Do not ask:

```text
Which database is best?
```

Ask:

```text
What queries must be fast?
What writes must be atomic?
What consistency is required?
What is the data shape?
How will it grow?
How will it be partitioned?
How painful are schema changes?
What operational burden can we accept?
```

## Database Types

| Type | Examples | Best For | Avoid When |
|---|---|---|---|
| Relational OLTP | PostgreSQL, MySQL | transactions, relational data, constraints, joins | massive write scale without partition planning |
| Document DB | MongoDB | flexible nested documents, aggregate-oriented reads | complex joins and cross-document consistency |
| Key-value DB | Redis, DynamoDB | fast lookup by key, sessions, counters, high-scale access patterns | ad-hoc querying |
| Wide-column | Cassandra, ScyllaDB | high-write distributed workloads, time-series-like access | joins, transactions, changing query patterns |
| Search engine | Elasticsearch, OpenSearch | text search, filtering, relevance ranking | source-of-truth transactions |
| Time-series DB | TimescaleDB, InfluxDB | metrics, events over time, retention/downsampling | complex relational transactions |
| Graph DB | Neo4j, Neptune | relationship-heavy traversal | simple CRUD or analytics better served elsewhere |
| Object storage | S3, GCS, Azure Blob | files, images, logs, backups, large immutable blobs | low-latency row-level updates |
| Vector DB | pgvector, Pinecone, Weaviate, Milvus | semantic search, RAG, embeddings | transactional source of truth |
| Data warehouse | BigQuery, Snowflake, Redshift | analytics and BI | user-facing low-latency transactions |

## Postgres as Default

Postgres is often the best default because it gives you:

- ACID transactions
- joins
- constraints
- indexes
- JSONB when needed
- full-text search for moderate needs
- partitioning
- extensions like `pgvector`
- strong ecosystem

Use Postgres when:

- relationships matter
- correctness matters
- access patterns are still evolving
- you need transactions
- you need operational simplicity

Do not prematurely replace Postgres just because a system is "large." Many scale problems are index, query, pooling, partitioning, or caching problems first.

## MongoDB

Use MongoDB when:

- your data is naturally document-shaped
- reads usually fetch whole aggregates
- schema changes frequently
- embedding related data reduces joins
- eventual consistency between aggregates is acceptable

Be careful when:

- you need many joins
- you need strict multi-document invariants
- documents grow without bound
- shard key is unclear
- access patterns are not known

Bad MongoDB design:

```text
Use MongoDB because frontend sends JSON.
```

Better MongoDB design:

```text
Use MongoDB because product catalog items are aggregate documents,
read mostly as complete documents,
with flexible attributes by category.
```

## DynamoDB

DynamoDB is access-pattern-first.

You do not model it like normalized SQL. You model around queries:

```text
PK = TENANT#123
SK = ORDER#2026-05-31#ORDER123
```

Use DynamoDB when:

- access patterns are known
- key-value or hierarchical access dominates
- extreme scale and low operational burden matter
- queries are mostly by partition key and sort key
- denormalization is acceptable

Be careful when:

- product queries change often
- you need ad-hoc querying
- hot partition risk is high
- global secondary indexes become uncontrolled
- multi-item transactions become central

## Elasticsearch / OpenSearch

Use search engines when:

- users search text
- relevance ranking matters
- filtering and faceting matter
- logs need search
- exact DB indexes are not enough

Do not use search engines as the source of truth for transactional data.

Good pattern:

```text
Postgres = source of truth
Kafka/outbox = change stream
Elasticsearch = search projection
```

## Database Choice Cheat Sheet

| Requirement | Good Starting Choice |
|---|---|
| Money movement | Postgres |
| Order lifecycle | Postgres |
| User/session cache | Redis |
| Product catalog with flexible attributes | MongoDB or Postgres JSONB |
| Full-text search | Elasticsearch/OpenSearch |
| Event analytics | Kafka + ClickHouse/BigQuery |
| Metrics | Prometheus/TimescaleDB/ClickHouse |
| Chat messages | Postgres first, then Cassandra/Scylla for huge scale |
| Real-time leaderboard | Redis sorted set + durable DB |
| AI document metadata | Postgres |
| AI vector search | pgvector first, dedicated vector DB if scale demands |
| Serverless high-scale key-value | DynamoDB |
| File storage | Object storage |

## Reading Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)
- [PostgreSQL Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [MongoDB Data Modeling](https://www.mongodb.com/docs/manual/data-modeling/)
- [MongoDB Sharding](https://www.mongodb.com/docs/manual/sharding/)
- [DynamoDB Data Modeling Foundations](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/data-modeling-foundations.html)
- [DynamoDB Partitions and Data Distribution](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.Partitions.html)
- [Elasticsearch Guide](https://www.elastic.co/guide/index.html)
- [Redis Data Types](https://redis.io/docs/latest/develop/data-types/)

## Tracker

- [ ] I can explain when to use Postgres
- [ ] I can explain when to use MongoDB
- [ ] I can explain when to use DynamoDB
- [ ] I can explain when to use Elasticsearch
- [ ] I can distinguish source-of-truth stores from projections
- [ ] I can model access patterns before choosing a database

---

# Level 3: Consistency, CAP, and Distributed Tradeoffs

## Goal

Understand what can go wrong when data is replicated, partitioned, cached, or processed asynchronously.

## CAP Theorem Without the Nonsense

CAP says that when a network partition happens, a distributed data system must choose between:

- consistency: every read sees the latest correct write
- availability: every request receives a non-error response

Partition tolerance is not optional in real distributed systems. Networks fail. The practical tradeoff during partition is usually:

```text
Do we reject/stop some operations to preserve correctness?
or
Do we accept operations and reconcile later?
```

## What People Get Wrong About CAP

Wrong:

```text
Pick any two of C, A, and P.
```

Better:

```text
When a partition occurs, you choose whether to preserve consistency or availability
for a particular operation.
```

CAP is not a full database selection framework. You also need latency, normal-case consistency, replication model, failure recovery, operational complexity, and business correctness.

## PACELC

PACELC extends the thinking:

```text
If Partition: choose Availability or Consistency.
Else: choose Latency or Consistency.
```

This matters because even when there is no partition, stronger consistency can cost latency.

## Consistency Models

| Model | Meaning | Example Use |
|---|---|---|
| Strong consistency | Reads reflect latest committed write | bank balance, inventory reservation |
| Eventual consistency | Replicas converge later | likes count, analytics |
| Read-your-writes | User sees their own update | profile edit |
| Monotonic reads | User does not go backward in time | notification read state |
| Causal consistency | Cause-effect order preserved | comment replies |
| Linearizability | Operations appear instant and globally ordered | locks, leader election |
| Serializability | Transactions behave as if run one at a time | financial transactions |

## Replication Patterns

| Pattern | Pros | Cons |
|---|---|---|
| Single leader | Simple writes, strong consistency easier | leader bottleneck/failover |
| Multi-leader | Local writes in multiple regions | conflict resolution hard |
| Leaderless/quorum | High availability and tunable consistency | read repair/conflict complexity |
| Async replication | Fast writes | stale reads and data loss window |
| Sync replication | safer writes | higher latency |

## Practical Examples

Payment charge:

```text
Prefer consistency.
Never double-charge.
Use idempotency key.
Use transaction or durable state machine.
```

Like count:

```text
Prefer availability.
Accept temporary stale count.
Reconcile asynchronously.
```

Inventory:

```text
Depends.
Limited-stock item needs strong reservation.
Large-stock item can use async correction.
```

## Reading Resources

- [Perspectives on the CAP Theorem](https://groups.csail.mit.edu/tds/papers/Gilbert/Brewer2.pdf)
- [PostgreSQL Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [MongoDB Read Concern](https://www.mongodb.com/docs/manual/reference/read-concern/)
- [MongoDB Write Concern](https://www.mongodb.com/docs/manual/reference/write-concern/)
- [DynamoDB Read Consistency](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html)

## Tracker

- [ ] I understand what CAP actually says
- [ ] I understand why partition tolerance is not optional
- [ ] I understand strong vs eventual consistency
- [ ] I understand read-your-writes
- [ ] I understand quorum tradeoffs
- [ ] I can choose consistency per operation

---

# Level 4: Caching and Redis

## Goal

Use caching to improve latency and reduce load without breaking correctness.

## Cache Patterns

| Pattern | How It Works | Use Case | Risk |
|---|---|---|---|
| Cache-aside | App checks cache, then DB, then fills cache | common reads | stale data |
| Read-through | Cache layer loads from DB | simpler app logic | cache dependency |
| Write-through | Write cache and DB together | consistency-sensitive reads | write latency |
| Write-behind | Write cache first, flush later | high write throughput | data loss risk |
| Refresh-ahead | Refresh before expiry | hot keys | complexity |
| Negative caching | Cache misses | reduce repeated misses | stale absence |

## Cache Failure Modes

| Failure | Meaning | Mitigation |
|---|---|---|
| Cache stampede | Many requests recompute same key | locks, singleflight, stale-while-revalidate |
| Hot key | One key receives huge traffic | replication, sharding, local cache |
| Thundering herd | Many keys expire together | TTL jitter |
| Stale cache | Cache returns old data | invalidation, short TTL, versioned keys |
| Cache penetration | Requests for nonexistent keys hit DB | negative cache, Bloom filter |
| Cache avalanche | Many keys disappear at once | stagger TTL, capacity planning |

## Redis Data Structures

| Redis Type | Backend Use |
|---|---|
| String | cache value, counter, lock token |
| Hash | small object fields |
| List | simple queue/stack |
| Set | uniqueness, membership |
| Sorted set | leaderboard, delayed jobs, rate windows |
| Stream | durable append-only event stream with consumer groups |
| Pub/Sub | fire-and-forget broadcast |
| Bitmap | compact flags |
| HyperLogLog | approximate cardinality |

## Redis as Cache vs Source of Truth

Redis can persist data, but treat it carefully.

Good Redis use:

```text
cache
session store
rate limiter
distributed lock with care
leaderboard
ephemeral job queue
stream for moderate durable events
```

Risky Redis use:

```text
primary database for irreversible money movement
only copy of critical jobs without persistence strategy
large unbounded queues without memory planning
distributed lock without fencing tokens
```

## Redis Queues

Redis queue options:

| Option | How It Works | Best For | Risk |
|---|---|---|---|
| List with LPUSH/BRPOP | simple blocking queue | simple jobs | weak delivery tracking |
| Sorted set | score as timestamp/priority | delayed jobs, scheduling | need claim/retry logic |
| Stream | append-only log + consumer groups | more durable event processing | more operational complexity |
| Pub/Sub | push messages to subscribers | ephemeral notifications | messages lost if subscriber offline |
| BullMQ | Redis-backed job queue library | Node.js background jobs | Redis capacity and job semantics matter |

## BullMQ

BullMQ is good when:

- Node.js/TypeScript stack
- background jobs
- retries
- delayed jobs
- repeatable jobs
- job priorities
- worker concurrency
- local product backend scale

Be careful when:

- jobs are mission-critical and long-retention
- throughput is event-stream scale
- Redis memory pressure is likely
- cross-language consumers are required
- you need durable replay across many teams

BullMQ is not Kafka. BullMQ is a job queue. Kafka is a distributed event log.

## Reading Resources

- [Redis Data Types](https://redis.io/docs/latest/develop/data-types/)
- [Redis Streams](https://redis.io/docs/latest/develop/data-types/streams/)
- [Redis Pub/Sub](https://redis.io/docs/latest/develop/pubsub/)
- [Redis Distributed Locks](https://redis.io/docs/latest/develop/use/patterns/distributed-locks/)
- [BullMQ Documentation](https://docs.bullmq.io/)
- [BullMQ Queues](https://docs.bullmq.io/guide/queues)
- [BullMQ Connections](https://docs.bullmq.io/guide/connections)

## Tracker

- [ ] I understand cache-aside
- [ ] I understand cache invalidation problems
- [ ] I understand TTL jitter
- [ ] I understand Redis strings, hashes, sets, sorted sets, streams, pub/sub
- [ ] I can choose between Redis list, stream, pub/sub, and BullMQ
- [ ] I understand why Redis is risky as a source of truth

---

# Level 5: Queues and Background Jobs

## Goal

Design async work that survives retries, crashes, spikes, and partial downstream failures.

## Queue Mental Model

```text
producer
-> broker/queue
-> consumer/worker
-> ack/delete/commit after success
```

A queue decouples producer speed from consumer speed.

## Queue Use Cases

- send emails
- process images/videos
- call slow third-party APIs
- generate reports
- run fraud checks
- sync search indexes
- retry failed webhooks
- process payments safely
- ingest AI documents
- batch notifications

## Delivery Semantics

| Semantic | Meaning | Reality |
|---|---|---|
| At-most-once | Message may be lost, never duplicated | rare for important work |
| At-least-once | Message will be retried, duplicates possible | most common |
| Exactly-once | Processed once in effect | usually achieved with idempotency, not magic |

Most production queue systems are at-least-once. Your handler must be idempotent.

## Ack, Nack, and Visibility Timeout

Traditional broker:

```text
consumer receives message
consumer processes
consumer ACKs success
broker removes message
```

If consumer fails before ACK:

```text
message is re-delivered
```

SQS-style visibility timeout:

```text
consumer receives message
message becomes invisible temporarily
consumer deletes message after success
if not deleted before timeout, message becomes visible again
```

## Retry Design

Bad retry:

```text
retry forever immediately
```

Good retry:

```text
retry with exponential backoff
limit attempts
send poison messages to DLQ
make handler idempotent
alert on DLQ growth
provide replay tooling
```

## Dead Letter Queue

A DLQ is for messages that could not be processed after max retries.

DLQ design must include:

- why it failed
- original payload
- retry count
- error type
- created time
- last failure time
- replay process
- alerting

## Push vs Pull Queues

| Model | How It Works | Best For | Risk |
|---|---|---|---|
| Pull | Consumers ask for work | consumer controls rate, good backpressure | polling latency |
| Push | Broker sends work to consumers | low latency, simple subscriber model | consumer overload if not controlled |

Pull is common for queues because workers can control how much work they take.

Push is common for pub/sub and webhook-style delivery, but must handle retries, backpressure, and slow subscribers.

## RabbitMQ vs SQS vs BullMQ vs Kafka

| System | Best For | Not Best For |
|---|---|---|
| RabbitMQ | routing, work queues, pub/sub exchange patterns, AMQP | long-term event replay |
| SQS | managed durable queue, simple async work, serverless | complex routing or stream processing |
| BullMQ | Node.js Redis-backed job processing | multi-team event streaming |
| Kafka | durable event log, replay, many consumers, high throughput | simple delayed jobs or task queues |

## Reading Resources

- [RabbitMQ Tutorials](https://www.rabbitmq.com/tutorials)
- [RabbitMQ Work Queues](https://www.rabbitmq.com/tutorials/tutorial-two-javascript)
- [RabbitMQ Publish/Subscribe](https://www.rabbitmq.com/tutorials/tutorial-three-javascript)
- [Amazon SQS Queue Types](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-queue-types.html)
- [Amazon SQS Visibility Timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html)
- [Amazon SQS Dead-Letter Queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html)
- [BullMQ Documentation](https://docs.bullmq.io/)

## Tracker

- [ ] I understand at-least-once delivery
- [ ] I understand ACK and visibility timeout
- [ ] I can design retries and DLQs
- [ ] I can explain push vs pull queues
- [ ] I can choose between SQS, RabbitMQ, BullMQ, and Kafka
- [ ] I can design idempotent workers

---

# Level 6: Kafka and Event Streaming

## Goal

Understand Kafka as a durable distributed log, not just a queue.

## Kafka Mental Model

```text
topic = named stream of records
partition = ordered append-only log
offset = position in partition
producer = writes records
consumer = reads records
consumer group = set of consumers sharing work
broker = Kafka server
replica = copy of partition
leader = broker handling reads/writes for a partition
```

## Kafka Is Not Just a Queue

Queue:

```text
message is consumed and removed
```

Kafka:

```text
message remains for retention period
consumers track offsets
new consumers can replay old messages
multiple consumer groups can independently read same events
```

## Partitions and Ordering

Ordering is guaranteed within a partition, not across the whole topic.

If order matters for a user:

```text
message key = user_id
```

That sends all events for the same user to the same partition, preserving per-user order.

Tradeoff:

```text
more ordering guarantee
= less parallelism for that key
```

## Consumer Groups

Within one consumer group:

```text
each partition is consumed by at most one consumer at a time
```

Across different consumer groups:

```text
each group receives its own copy of the event stream
```

Example:

```text
Topic: order-events

Consumer group A: email-service
Consumer group B: analytics-service
Consumer group C: warehouse-service

All groups read the same events independently.
Within each group, partitions are distributed among instances.
```

## Kafka Fan-Out

Kafka fan-out happens through multiple consumer groups.

```text
OrderCreated event
-> email-service group
-> analytics-service group
-> warehouse-service group
-> fraud-service group
```

Each group can process at its own pace.

## Kafka Fan-In

Fan-in means many producers or streams feed into one downstream processor.

Examples:

```text
mobile-events
web-events
server-events
-> unified-user-activity topic
```

or:

```text
orders
payments
shipments
-> customer-timeline materialized view
```

## Kafka Failure Design

Important questions:

- When do you commit offsets?
- Is processing idempotent?
- What happens if processing succeeds but offset commit fails?
- What happens if offset commit succeeds but DB write fails?
- How do you handle poison messages?
- Do you need retry topics?
- Do you need a DLQ topic?
- Can messages be replayed safely?

## Kafka vs Queue

Use Kafka when:

- events are valuable beyond one consumer
- replay matters
- throughput is high
- multiple teams consume same event stream
- event history is needed
- stream processing is required

Use a queue when:

- work item has one logical consumer group
- task should disappear after success
- delayed retries are central
- worker semantics matter more than event history

## Kafka Anti-Patterns

- using Kafka for simple delayed jobs
- putting huge payloads directly in Kafka
- designing topics without ownership
- no schema/version strategy
- no idempotent consumers
- committing offsets before durable side effects
- assuming global ordering
- using too few partitions and then needing more parallelism
- using too many partitions and making operations harder

## Reading Resources

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Kafka Introduction](https://kafka.apache.org/documentation/#intro_concepts_and_terms)
- [Confluent Kafka Consumer Design](https://docs.confluent.io/kafka/design/consumer-design.html)
- [Kafka Streams Documentation](https://kafka.apache.org/documentation/streams/)

## Tracker

- [ ] I understand topics, partitions, offsets, and brokers
- [ ] I understand consumer groups
- [ ] I understand partition-level ordering
- [ ] I understand replay
- [ ] I can design retry and DLQ topics
- [ ] I can explain Kafka vs queue

---

# Level 7: Fan-In, Fan-Out, Push, and Pull

## Goal

Design systems where work branches out, aggregates back, or is delivered to many consumers.

## Fan-Out

Fan-out means one event triggers many downstream actions.

Example:

```text
UserUploadedVideo
-> transcode video
-> generate thumbnails
-> scan for policy violations
-> extract transcript
-> update search index
-> notify followers
```

Fan-out options:

| Option | How It Works | Good For |
|---|---|---|
| SNS -> SQS | One topic pushes to many queues | AWS managed fan-out |
| Kafka topic -> many consumer groups | Consumers independently read same stream | durable event fan-out |
| RabbitMQ fanout exchange | Exchange broadcasts to bound queues | broker-level routing |
| App-level fan-out | Application writes many jobs | more control, more coupling |

## Fan-In

Fan-in means many branches or producers converge.

Example:

```text
thumbnail job
transcode job
moderation job
transcript job
-> all complete
-> publish VideoReady
```

You need state tracking:

```text
workflow_id
required_steps
completed_steps
failed_steps
timeout_at
```

Common storage:

- Postgres row with status
- DynamoDB item with step states
- Redis for ephemeral coordination
- workflow engine for complex cases

## Push Delivery

Push means server/broker sends data to consumers.

Examples:

- WebSocket updates
- webhooks
- SNS pushing to Lambda/HTTP/SQS
- RabbitMQ delivering messages to subscribed consumers

Benefits:

- low latency
- efficient when updates are rare but important
- natural for real-time systems

Risks:

- consumer overload
- retry storms
- slow subscribers
- connection management
- backpressure complexity

## Pull Delivery

Pull means consumers ask for data/work.

Examples:

- SQS workers polling messages
- Kafka consumers polling records
- clients polling API
- batch ETL pulling new records

Benefits:

- consumer controls rate
- backpressure is easier
- batch processing is natural

Risks:

- polling latency
- wasted requests
- needs cursor/offset/checkpoint handling

## Modern Pattern: Push Notification + Pull State

For real-time apps, a strong pattern is:

```text
push lightweight notification
client pulls canonical state
```

Example:

```text
WebSocket event: document_changed
Client fetches latest document state via API
```

This avoids putting too much truth into transient push messages.

## Reading Resources

- [Amazon SNS Fanout to SQS](https://docs.aws.amazon.com/sns/latest/dg/sns-sqs-as-subscriber.html)
- [Amazon SNS Fanout to Lambda](https://docs.aws.amazon.com/sns/latest/dg/sns-lambda-as-subscriber.html)
- [RabbitMQ Publish/Subscribe](https://www.rabbitmq.com/tutorials/tutorial-three-javascript)
- [Amazon Kinesis Enhanced Fan-Out](https://docs.aws.amazon.com/streams/latest/dev/enhanced-consumers.html)

## Tracker

- [ ] I understand fan-out
- [ ] I understand fan-in
- [ ] I can design state tracking for fan-in
- [ ] I understand push delivery
- [ ] I understand pull delivery
- [ ] I can combine push notifications with pull state

---

# Level 8: Scaling, Partitioning, and Hotspots

# Level 8: Sockets and Real-Time Broadcasting

## Goal

Design real-time systems that support live updates without confusing transient delivery with durable truth.

Sockets are not just "REST but faster." They introduce a different set of problems:

- long-lived connections
- connection state
- rooms/channels
- authentication over time
- reconnects
- missed events
- backpressure
- horizontal scaling
- broadcast fan-out
- presence correctness
- delivery guarantees

## Inductive Starting Problem

Start with a simple notification API:

```text
Client calls GET /notifications every 30 seconds.
```

This works early.

Then product asks:

```text
Show new notifications instantly.
Show online users.
Show typing indicators.
Update dashboard counters live.
Support collaborative editing.
```

Polling starts to hurt:

- too many useless requests
- updates feel delayed
- backend load grows even when nothing changes
- presence is awkward
- collaborative editing is almost impossible

Now you earn real-time communication.

---

## TCP Sockets vs WebSockets vs SSE vs Polling

| Method | Direction | Best For | Avoid When |
|---|---|---|---|
| Raw TCP socket | bidirectional | custom protocols, infra/internal systems | browser apps, normal web products |
| WebSocket | bidirectional | chat, collaboration, multiplayer, live dashboards | simple one-way updates |
| Server-Sent Events | server -> client | notifications, live feeds, status updates | client must send frequent real-time messages |
| Long polling | mostly server -> client | compatibility, simple near-real-time | high scale with frequent updates |
| Short polling | client repeatedly asks | simple status refresh | low-latency real-time needs |
| Webhook | server -> server | third-party async integration | browser/user live updates |

## Rule of Thumb

Use WebSockets when:

- client and server both send frequent real-time messages
- rooms/channels matter
- presence matters
- low-latency interaction matters

Use SSE when:

- server mostly pushes updates
- client does not need full bidirectional real-time messaging
- you want simpler browser behavior than WebSockets

Use polling when:

- updates are rare
- latency requirements are loose
- simplicity beats efficiency

Use webhooks when:

- another backend needs to be notified
- not a browser client

---

## WebSocket Mental Model

```text
HTTP request starts connection
server upgrades to WebSocket
connection stays open
client and server exchange messages
connection eventually closes
client reconnects
```

Unlike REST:

```text
REST request has short-lived state.
WebSocket connection has long-lived state.
```

That means you must track:

- connection ID
- user ID
- tenant ID
- subscribed rooms
- auth expiry
- last heartbeat
- server node holding connection
- backpressure state

---

## Real-Time Message Types

Not all socket messages are equal.

| Message Type | Durable? | Example |
|---|---|---|
| Typing indicator | no | user is typing |
| Presence heartbeat | no | user is online |
| Notification signal | maybe | new notification available |
| Chat message | yes | user sent message |
| Collaborative edit operation | yes | insert text at position |
| Dashboard counter update | derived | active users count changed |
| System command | yes | force logout, role changed |

## Important Rule

Do not treat every WebSocket message as durable business truth.

A safe pattern:

```text
Durable event goes to database/log.
Socket broadcasts lightweight update.
Client pulls or confirms canonical state when needed.
```

Example:

```text
Chat message:
1. Client sends message over WebSocket or HTTP.
2. Server stores message in database.
3. Server broadcasts MessageCreated to room.
4. Clients render it.
5. On reconnect, clients fetch missed messages from API.
```

---

## Rooms, Channels, and Topics

Rooms are server-side groups of connections.

Examples:

```text
user:123
tenant:acme
document:doc_456
project:proj_789
conversation:conv_999
dashboard:ops
```

Use rooms when:

- only some users should receive an event
- authorization must be scoped
- broadcast target is meaningful

Room join checklist:

- [ ] authenticate user
- [ ] authorize access to room
- [ ] record connection membership
- [ ] handle disconnect cleanup
- [ ] handle permission changes while connected

## Broadcasting Types

| Broadcast Type | Meaning | Example |
|---|---|---|
| One-to-one | send to one user/device | direct notification |
| One-to-room | send to all connections in a room | chat message |
| One-to-tenant | send to all users in tenant | admin announcement |
| One-to-many selected | send to filtered users | role-based update |
| Global broadcast | send to everyone | outage banner |
| Excluding sender | send to everyone except origin client | typing indicator |

## Broadcasting Cost

Broadcasting multiplies work.

```text
1 event to 10 users = 10 sends
1 event to 10,000 users = 10,000 sends
1 event to 1,000,000 users = now you have a platform problem
```

Design questions:

- How many recipients per event?
- Is every recipient online?
- Can messages be batched?
- Can clients pull instead?
- Can we broadcast only an invalidation signal?
- Do we need per-user personalization?

---

## Presence and Online Status

Presence sounds simple and is secretly slippery.

Naive:

```text
on connect -> user online
on disconnect -> user offline
```

Problems:

- mobile networks drop silently
- browser tabs sleep
- user has multiple devices
- user has multiple tabs
- server crashes before disconnect cleanup
- load balancer closes idle connections

Better presence model:

```text
connection heartbeat every N seconds
store connection presence with TTL
user is online if at least one active connection exists
```

Redis pattern:

```text
presence:user:123:conn:abc -> TTL 60s
```

User online check:

```text
exists any active connection key for user
```

For large systems, avoid checking all keys frequently. Maintain counters carefully:

```text
user_connection_count
tenant_online_count
```

But counters require cleanup/reconciliation.

## Presence Types

| Type | Accuracy Needed |
|---|---|
| Green dot online | approximate is fine |
| Typing indicator | ephemeral is fine |
| Agent availability in support system | more accurate |
| Multiplayer game session | highly accurate |
| Compliance/audit presence | needs durable records |

---

## Heartbeats and Timeouts

Heartbeats detect dead connections.

Typical flow:

```text
server sends ping
client responds pong
if no response within timeout, close connection
```

You need heartbeats because TCP connections can appear alive after the client disappears.

Track:

- last ping time
- last pong time
- missed heartbeat count
- connection age
- reconnect frequency

---

## Reconnect and Resume

Clients disconnect. Always.

Reasons:

- mobile network changes
- laptop sleeps
- server deploys
- load balancer timeout
- tab suspended
- Wi-Fi switches

Bad design:

```text
If client disconnects, it misses everything forever.
```

Better design:

```text
Client reconnects with last_seen_event_id.
Server sends missed durable events or tells client to resync.
```

Example:

```text
client reconnect payload:
{
  "user_id": "u1",
  "last_seen_message_id": "msg_123",
  "rooms": ["conversation:c1"]
}
```

Server:

```text
1. authenticate
2. re-authorize rooms
3. fetch missed messages after msg_123
4. send missed events
5. resume live stream
```

If gap is too large:

```text
send resync_required
client fetches full canonical state
```

---

## Delivery Guarantees

WebSocket by itself does not solve durable delivery.

| Guarantee | How To Approach |
|---|---|
| Fire-and-forget | send socket event, no ack |
| At-least-once | server retries until client ack |
| At-most-once | send once, no retry |
| Exactly-once effect | idempotent event IDs and client/server dedupe |
| Ordered per room | sequence numbers per room |
| Resume after disconnect | durable event log + cursor |

## Client ACKs

Use ACKs when delivery matters.

```text
server -> event { id: 101, type: MessageCreated }
client -> ack { id: 101 }
```

But ACKs create state:

- pending messages
- retry timers
- duplicate handling
- memory pressure
- slow client problems

Use ACKs selectively, not for every typing indicator.

## Sequence Numbers

For ordered rooms:

```text
conversation:c1 sequence = 1001, 1002, 1003
```

Client can detect gaps:

```text
received 1001
received 1003
missing 1002 -> request resync
```

---

## Horizontal Scaling

With one server:

```text
all connections live in one process
broadcast is simple
```

With many servers:

```text
user A connected to node 1
user B connected to node 2
event produced on node 3
all relevant nodes must know what to send
```

Now you need a socket gateway architecture.

## Common Architecture

```text
clients
-> load balancer
-> WebSocket gateway nodes
-> Redis Pub/Sub or Kafka or NATS for cross-node events
-> application services
-> database/source of truth
```

## Sticky Sessions

Sticky sessions keep a client connected to the same server.

Useful because:

- connection state is local
- simpler room membership

But:

- server crash still disconnects clients
- scaling/rebalancing is harder
- you still need cross-node broadcast

Sticky sessions help, but they do not remove the need for shared coordination.

## Cross-Node Broadcast Options

| Tool | Best For | Risk |
|---|---|---|
| Redis Pub/Sub | ephemeral cross-node socket broadcast | no replay |
| Redis Streams | durable-ish stream with consumer groups | more complexity |
| Kafka | durable event backbone, replay, many consumers | heavier |
| NATS | lightweight messaging, request/reply, pub/sub | operational learning |
| Database polling | simple low-scale invalidation | latency and DB load |

## Redis Pub/Sub Adapter Pattern

```text
Node 1 receives chat message
Node 1 stores message in DB
Node 1 publishes socket_event to Redis channel conversation:c1
All socket nodes subscribed receive event
Each node sends event to local connections in room conversation:c1
```

Important:

Redis Pub/Sub is not durable. If a node is offline, it misses the message.

That is okay if the durable truth is in DB and clients can resync.

---

## Socket Gateway vs Business Service

Avoid putting all business logic in the socket server.

Better split:

```text
Socket Gateway:
- connection management
- auth handshake
- room join/leave
- sending/receiving realtime messages
- heartbeat

Business Services:
- validate business commands
- write database
- publish durable events
- enforce permissions
```

Example:

```text
client sends SendMessage over WebSocket
socket gateway authenticates connection
chat service validates conversation membership
chat service writes message to DB
chat service publishes MessageCreated
socket gateway broadcasts MessageCreated
```

---

## Backpressure and Slow Clients

A slow client can hurt your server.

Problems:

- send buffer grows
- memory increases
- latency increases
- event loop blocks in Node.js
- one connection degrades others

Mitigations:

- max outbound queue per connection
- drop low-priority events
- compress carefully
- batch updates
- disconnect very slow clients
- send invalidation instead of full payload
- use per-room rate limits

Message priority:

| Priority | Example | Action Under Pressure |
|---|---|---|
| Critical | force logout, permission revoked | keep |
| Durable | chat message created | keep or resync |
| State invalidation | document changed | coalesce |
| Ephemeral | typing, cursor movement | drop |

---

## Authentication and Authorization

WebSocket auth has two phases:

```text
1. authenticate connection
2. authorize room/action
```

Do not assume:

```text
connected user can join any room
```

Room authorization examples:

- user belongs to tenant
- user has access to document
- user is participant in conversation
- user has dashboard permission

Auth expiry problem:

```text
JWT expires while socket remains open
```

Options:

- close socket when token expires
- require token refresh message
- periodically revalidate session
- revoke connections on permission change

## Security Checklist

- [ ] authenticate during handshake
- [ ] authorize every room join
- [ ] validate every inbound message schema
- [ ] rate limit messages per connection/user
- [ ] enforce max payload size
- [ ] do not trust client-supplied user_id
- [ ] handle token expiry
- [ ] support force disconnect
- [ ] prevent tenant cross-broadcast

---

## Socket Observability

Track:

- active connections
- connections per node
- connections per tenant
- reconnect rate
- average connection duration
- heartbeat failures
- room count
- members per room
- messages sent/sec
- messages received/sec
- dropped messages
- outbound buffer size
- Redis Pub/Sub lag or errors
- auth failures
- unauthorized join attempts

Useful alerts:

- reconnect storm
- one node has too many connections
- outbound buffers growing
- heartbeat failures spike
- Redis adapter unavailable
- unauthorized join attempts spike

---

## When Not To Use WebSockets

Avoid WebSockets when:

- simple polling every few minutes is enough
- only server-to-client updates are needed and SSE is simpler
- clients are unreliable and durable delivery matters more than latency
- infrastructure cannot support long-lived connections
- you do not have a reconnection/resync strategy
- the team has no operational readiness for connection-heavy systems

Sometimes this is enough:

```text
POST /job
GET /job/{id}/status every 5 seconds
```

Not everything needs a socket. The little architecture goblin in our heads likes shiny persistent connections, but production makes us pay rent on them.

---

## Real-Time Design Patterns

## Pattern 1: Chat

```text
client sends message
-> server validates membership
-> message stored in DB
-> event published
-> socket nodes broadcast to conversation room
-> clients ACK or fetch missed messages on reconnect
```

Core choices:

- durable messages in DB
- WebSocket for live delivery
- sequence IDs per conversation
- reconnect with last_seen_message_id

## Pattern 2: Presence

```text
connect -> create presence key with TTL
heartbeat -> refresh TTL
disconnect -> remove key if possible
periodic cleanup -> correct stale state
```

Core choices:

- approximate is usually acceptable
- multiple connections per user
- TTL avoids permanent ghost users

## Pattern 3: Live Dashboard

```text
backend events
-> aggregator updates counters
-> socket broadcasts compact updates
-> client periodically refreshes full dashboard state
```

Core choices:

- do not send every raw event to every dashboard
- aggregate before broadcasting
- coalesce frequent updates

## Pattern 4: Collaborative Editing

```text
client sends operation
-> validate permission
-> apply CRDT/OT logic
-> store operation log
-> broadcast operation to document room
-> snapshot periodically
```

Core choices:

- operations must be durable
- order/versioning matters
- reconnect requires operation replay or snapshot fetch

## Pattern 5: Notification Bell

```text
notification created in DB
-> socket sends notification_count_changed
-> client fetches latest notification list
```

Core choices:

- socket event is a signal
- API remains canonical source
- missed socket event is okay because client can fetch

---

## Reading Resources

- [MDN WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [MDN Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [Socket.IO Documentation](https://socket.io/docs/v4/)
- [Socket.IO Rooms](https://socket.io/docs/v4/rooms/)
- [Socket.IO Redis Adapter](https://socket.io/docs/v4/redis-adapter/)
- [Redis Pub/Sub](https://redis.io/docs/latest/develop/pubsub/)
- [Redis Streams](https://redis.io/docs/latest/develop/data-types/streams/)
- [NATS Documentation](https://docs.nats.io/)

## Tracker

- [ ] I can choose between WebSocket, SSE, polling, and webhook
- [ ] I understand rooms/channels
- [ ] I can design one-to-one and room broadcasts
- [ ] I understand presence with TTL and heartbeats
- [ ] I can design reconnect and resume
- [ ] I understand socket delivery guarantees
- [ ] I can scale sockets across multiple nodes
- [ ] I understand Redis Pub/Sub adapter limitations
- [ ] I can handle slow clients and backpressure
- [ ] I can secure socket room joins

---

# Level 9: Scaling, Partitioning, and Hotspots

## Goal

Scale by identifying bottlenecks and partitioning work/data correctly.

## Scaling Types

| Type | Meaning |
|---|---|
| Vertical scaling | Bigger machine |
| Horizontal scaling | More machines |
| Read scaling | replicas, caches, CDN |
| Write scaling | sharding, partitioning, batching, async |
| Storage scaling | partitioning, compaction, archiving |
| Consumer scaling | more workers, more partitions, batching |

## Partitioning

Partitioning splits data/work.

Good partition keys:

- high cardinality
- evenly distributed
- match access patterns
- avoid one tenant/user/item becoming too hot

Bad partition keys:

- status
- country if traffic is uneven
- date only for high-write workloads
- tenant_id if one tenant can dominate

## Hotspot Examples

Bad:

```text
PK = TODAY
all writes for today hit same partition
```

Better:

```text
PK = TODAY#bucket_0..bucket_99
```

Bad:

```text
Kafka key = event_type
all OrderCreated events hit same partition
```

Better:

```text
Kafka key = order_id or customer_id
```

Bad:

```text
Redis key = global_counter
millions of writes hit one key
```

Better:

```text
counter shards:
global_counter:0
global_counter:1
...
sum periodically
```

## Scaling Consumers

Queue worker scaling:

```text
increase workers
increase batch size
increase concurrency
reduce per-job latency
split queues by priority
```

Kafka scaling:

```text
increase partitions
increase consumer instances up to partition count
batch writes/reads
optimize processing
avoid hot keys
```

Important:

```text
In Kafka, adding more consumers than partitions in the same consumer group does not increase parallelism.
```

## Backpressure

Backpressure says:

```text
If downstream is slow, upstream must slow down, buffer, degrade, or reject.
```

Options:

- queue work
- rate limit producers
- shed low-priority traffic
- reduce quality
- batch more
- scale consumers
- pause ingestion
- use circuit breakers

## Tracker

- [ ] I can identify hot partitions
- [ ] I can choose good partition keys
- [ ] I understand Kafka partition scaling
- [ ] I understand queue worker scaling
- [ ] I can design backpressure
- [ ] I can shard counters and high-write keys

---

# Level 10: Reliability and Failure Handling

## Goal

Design systems that survive reality.

## Failure Types

| Failure | Example |
|---|---|
| Process crash | worker dies mid-job |
| Network failure | service cannot reach database |
| Timeout | dependency is slow |
| Partial failure | payment charged but order update failed |
| Duplicate delivery | same event processed twice |
| Out-of-order events | shipment arrives before payment event |
| Poison message | one message always crashes consumer |
| Data corruption | bad deployment writes invalid state |
| Retry storm | failure causes massive retry traffic |
| Split brain | two leaders believe they are active |

## Reliability Patterns

| Pattern | Use |
|---|---|
| Idempotency key | safe retries |
| Outbox pattern | publish event only after DB commit |
| Inbox pattern | deduplicate consumed messages |
| Saga | coordinate multi-step distributed workflow |
| Circuit breaker | stop calling failing dependency |
| Bulkhead | isolate failure domains |
| Timeout | prevent stuck calls |
| Retry with backoff | recover transient failures |
| DLQ | isolate poison messages |
| Compensating action | undo or correct previous step |
| Reconciliation job | compare systems and repair drift |

## Outbox Pattern

Problem:

```text
DB write succeeds
event publish fails
downstream systems never learn about change
```

Solution:

```text
within same DB transaction:
1. write business row
2. write outbox row

background publisher:
1. reads unpublished outbox rows
2. publishes events
3. marks rows published
```

This gives durable event publishing tied to the source-of-truth database.

## Inbox Pattern

Problem:

```text
consumer receives same message twice
```

Solution:

```text
store processed message_id
if already processed, skip side effect
otherwise process and record message_id
```

## Saga Pattern

Use sagas when one business process spans multiple services.

Example:

```text
create order
-> reserve inventory
-> charge payment
-> create shipment
```

If shipment fails:

```text
refund payment
release inventory
cancel order
```

Saga styles:

| Style | Meaning |
|---|---|
| Choreography | services react to events |
| Orchestration | central workflow controller tells services what to do |

Choreography is simpler early. Orchestration is clearer for complex workflows.

## Tracker

- [ ] I understand idempotency keys
- [ ] I understand outbox pattern
- [ ] I understand inbox pattern
- [ ] I understand sagas
- [ ] I can design retries without retry storms
- [ ] I can design reconciliation jobs

---

# Level 11: Observability and Operations

## Goal

Make systems debuggable and operable.

## The Three Pillars

| Pillar | Use |
|---|---|
| Logs | What happened |
| Metrics | How often and how much |
| Traces | Where time went across services |

## Metrics to Track

API:

- request rate
- error rate
- p50/p95/p99 latency
- timeout count
- saturation

Database:

- query latency
- slow queries
- lock waits
- connection pool usage
- replication lag
- index hit ratio

Queue:

- queue depth
- oldest message age
- processing rate
- retry count
- DLQ count
- consumer lag

Kafka:

- consumer lag
- broker disk usage
- under-replicated partitions
- request latency
- rebalance frequency
- produce/consume throughput

Redis:

- memory usage
- evictions
- hit rate
- command latency
- blocked clients
- keyspace size

## Alerting Rules

Alert on user impact and exhaustion:

- high error rate
- high p99 latency
- queue oldest age too high
- Kafka consumer lag growing
- DB connections saturated
- Redis evictions rising
- DLQ messages appearing
- disk nearing full

Avoid noisy alerts for harmless fluctuations.

## Runbook Template

```text
Alert:
User impact:
Dashboard:
First checks:
Common causes:
Safe mitigations:
Rollback steps:
Escalation:
Post-incident actions:
```

## Reading Resources

- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Google SRE Book: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)

## Tracker

- [ ] I can define useful API metrics
- [ ] I can define useful queue metrics
- [ ] I can define useful Kafka metrics
- [ ] I can define useful database metrics
- [ ] I can write a runbook
- [ ] I understand alert fatigue

---

# Level 12: Security, Multi-Tenancy, and Compliance

## Goal

Design systems where data is protected by default.

## Security Basics

- authentication: who are you?
- authorization: what can you access?
- encryption in transit
- encryption at rest
- secrets management
- audit logs
- least privilege
- rate limiting
- input validation
- tenant isolation

## Multi-Tenancy Models

| Model | Pros | Cons |
|---|---|---|
| Shared DB, shared schema | cheap, simple early | isolation must be perfect |
| Shared DB, separate schema | stronger separation | migrations harder |
| Separate DB per tenant | strong isolation | operational overhead |
| Separate account/project per tenant | strongest isolation | expensive and complex |

## Tenant Isolation Checklist

- [ ] Every query filters by tenant ID
- [ ] Background jobs include tenant context
- [ ] Queue messages include tenant ID
- [ ] Cache keys include tenant ID
- [ ] Search indexes enforce tenant filters
- [ ] Object storage paths include tenant scoping
- [ ] Admin actions are audited
- [ ] Cross-tenant analytics uses sanitized data

## PII Handling

Design questions:

- What data is PII?
- Do we need to store it?
- Can it be tokenized?
- Who can access it?
- Is it in logs?
- Is it in queue payloads?
- Is it in analytics?
- How is deletion handled?

## Tracker

- [ ] I can design authn/authz boundaries
- [ ] I can design tenant isolation
- [ ] I can avoid PII in logs and queues
- [ ] I can design audit trails
- [ ] I can choose a multi-tenancy model

---

# Modern System Design Problems

These are intentionally not generic URL shorteners. Each problem includes what to think about and what technologies are likely appropriate.

---

## Problem 1: AI Document Ingestion and RAG Platform

### Scenario

Users upload PDFs, docs, and webpages. The system parses, chunks, embeds, indexes, and serves question-answering with citations.

### Requirements

- upload large documents
- parse asynchronously
- chunk and embed text
- store source metadata
- vector search with tenant isolation
- answer questions with citations
- re-index when embeddings model changes
- handle failed parses
- track cost per tenant

### Design

```text
API
-> object storage for files
-> Postgres for document metadata
-> queue for parsing jobs
-> workers for parse/chunk/embed
-> vector store for embeddings
-> Redis for short-lived status cache
-> LLM provider for answers
-> eval pipeline for answer quality
```

### Queue Choice

Use BullMQ if:

- Node.js backend
- moderate workload
- simple retries/delays needed

Use SQS if:

- AWS managed infra
- durable simple job queue
- serverless workers

Use Kafka if:

- document events feed many downstream systems
- replay/reprocessing is central
- many teams consume the pipeline

### Database Choice

- Postgres for tenants, users, documents, permissions
- Object storage for original files
- pgvector for simple-to-medium vector search
- dedicated vector DB if scale/search requirements demand it

### Failure Cases

- parser crashes
- file is corrupt
- embedding provider rate limits
- vector insert succeeds but metadata update fails
- tenant deletes document during processing
- model version changes

### Key Patterns

- idempotent jobs by document_id + version
- DLQ for failed parses
- status state machine
- outbox event after document indexed
- reindex workflow
- tenant-aware retrieval

---

## Problem 2: Multi-Channel Notification Platform

### Scenario

Send notifications through email, SMS, push, WhatsApp, and in-app channels.

### Requirements

- user preferences
- quiet hours
- retries
- provider failover
- deduplication
- rate limits
- fan-out to many channels
- delivery receipts
- templates
- audit trail

### Design

```text
Notification API
-> Postgres for notification request and preferences
-> outbox event NotificationRequested
-> fan-out router
-> per-channel queues
-> provider workers
-> delivery status updates
-> analytics stream
```

### Fan-Out

```text
NotificationRequested
-> email queue
-> sms queue
-> push queue
-> in-app queue
```

Use separate queues per channel because each provider has different:

- latency
- rate limit
- retry behavior
- cost
- failure mode

### Push vs Pull

Provider workers pull from queues so they can control throughput.

Real-time in-app notifications can push over WebSocket/SSE, but client should pull canonical notification list after receiving a lightweight signal.

### Key Patterns

- idempotency key per notification/channel/user
- DLQ per provider
- retry with backoff
- provider circuit breaker
- dedupe window
- preference snapshot at send time
- delivery status state machine

---

## Problem 3: Payment Event Reconciliation System

### Scenario

Your system receives payment webhooks from Stripe/Razorpay/Adyen and must maintain correct order/payment state.

### Requirements

- no double charging
- handle duplicate webhooks
- handle out-of-order webhooks
- reconcile with provider API
- preserve audit trail
- update orders
- trigger downstream fulfillment

### Design

```text
Webhook endpoint
-> verify signature
-> store raw webhook event
-> enqueue processing
-> idempotent payment state machine
-> update order/payment transactionally
-> publish PaymentSucceeded/PaymentFailed
-> reconciliation job polls provider for mismatches
```

### Database Choice

Use Postgres.

Reason:

- transactions matter
- audit trail matters
- relational constraints matter
- correctness beats write scale early

### Queue Choice

SQS/RabbitMQ/BullMQ can work for processing webhooks.

Kafka is useful if payment events are consumed by many systems and replay is important.

### Key Patterns

- webhook event table with unique provider_event_id
- payment state machine
- idempotency keys
- row-level locking or optimistic concurrency
- outbox pattern for downstream events
- reconciliation job
- DLQ for malformed events

---

## Problem 4: Real-Time Collaborative Document Editing

### Scenario

Users edit documents together and see changes in real time.

### Requirements

- low latency collaboration
- presence indicators
- offline edits
- conflict resolution
- document history
- comments
- access control
- snapshots

### Design

```text
WebSocket gateway
-> collaboration service
-> Redis pub/sub for node-to-node ephemeral broadcast
-> durable operation log
-> snapshot storage
-> Postgres for documents/permissions
-> object storage for large snapshots if needed
```

### Important Choice

Redis Pub/Sub is fine for ephemeral presence and live signals.

Do not rely on Redis Pub/Sub as the only copy of document changes. If a subscriber is offline, messages are gone.

Use a durable operation log for edits.

### Push/Pull Pattern

```text
push operations over WebSocket
periodically persist durable operation log
clients pull latest snapshot when reconnecting
```

### Key Patterns

- CRDT or OT for conflict resolution
- versioned operations
- presence is ephemeral
- edits are durable
- permission check before joining doc room
- snapshot compaction

---

## Problem 5: Event Analytics Pipeline

### Scenario

Collect product events from web/mobile/backend and support dashboards, funnels, and near-real-time analytics.

### Requirements

- high write volume
- tolerate duplicate events
- handle late events
- support schema evolution
- real-time counters
- long-term analytics
- tenant isolation

### Design

```text
event collector API
-> Kafka/Kinesis
-> stream processors
-> real-time aggregates in Redis/ClickHouse
-> raw event storage in object storage
-> warehouse for long-term analytics
```

### Kafka Fit

Kafka fits because:

- events are durable
- multiple consumers need same stream
- replay matters
- high throughput matters

### Key Patterns

- event_id for dedupe
- schema registry or schema versioning
- partition by tenant_id or user_id depending on access
- late event handling
- raw immutable event log
- derived materialized views
- DLQ topic for invalid events

---

## Problem 6: Workflow Orchestration Engine

### Scenario

Users define workflows like:

```text
when invoice uploaded
-> extract fields
-> ask human to approve
-> send payment request
-> update ERP
```

### Requirements

- long-running workflows
- retries
- timers
- human approval
- step dependencies
- audit trail
- cancellation
- visibility into state

### Design

```text
Workflow API
-> Postgres workflow definitions
-> workflow instance state
-> job queue for executable steps
-> scheduler for timers
-> workers for activities
-> event log for audit
```

### Fan-In/Fan-Out

Fan-out:

```text
parallel steps start together
```

Fan-in:

```text
workflow continues only when required steps complete
```

### Key Patterns

- state machine
- idempotent step execution
- heartbeat for long tasks
- retry policy per step
- timeout policy per step
- compensation steps
- audit event log

---

## Problem 7: Personalized Feed and Ranking Backend

### Scenario

Build a feed for posts, videos, products, or jobs.

### Requirements

- personalized ranking
- freshness
- pagination
- fan-out to followers
- block/mute filters
- trending content
- abuse controls

### Design Options

Fan-out on write:

```text
when creator posts
-> write item to followers' feed inboxes
```

Good for:

- fast reads
- users with moderate follower counts

Bad for:

- celebrity accounts
- huge fan-out

Fan-out on read:

```text
when user opens feed
-> fetch followed creators' posts
-> rank dynamically
```

Good for:

- fresh ranking
- large creators

Bad for:

- slower reads

Hybrid:

```text
fan-out normal creators on write
pull celebrity/high-volume creators on read
```

### Data Stores

- Postgres for users, follows, posts metadata
- Redis sorted sets for feed candidates or hot rankings
- Elasticsearch/OpenSearch for search/discovery
- Kafka for feed events
- object storage/CDN for media

### Key Patterns

- cursor pagination
- ranking materialization
- fan-out control
- celebrity fallback
- dedupe candidates
- freshness decay
- moderation filters

---

## Problem 8: Fraud and Risk Event Pipeline

### Scenario

Score user actions for fraud risk in near real time.

### Requirements

- low-latency risk score
- ingest many event types
- enrich with user/device/IP history
- update risk features
- trigger manual review
- explain decisions
- avoid blocking all traffic when risk system is down

### Design

```text
event stream
-> feature builders
-> feature store/cache
-> risk scoring service
-> decision engine
-> review queue
-> audit log
```

### Database Choices

- Kafka for event stream
- Redis for hot features/counters
- Postgres for decisions and review cases
- warehouse/lake for model training
- graph DB optional for relationship-heavy fraud rings

### Key Patterns

- sliding window counters
- device/IP/user feature aggregation
- fallback risk policy
- circuit breaker
- async review queue
- audit every decision

---

## Problem 9: Large File/Video Processing Platform

### Scenario

Users upload large videos. System validates, transcodes, scans, thumbnails, extracts metadata, and publishes.

### Requirements

- resumable upload
- large object storage
- virus/moderation scan
- transcode variants
- thumbnails
- status tracking
- retries
- partial failures

### Design

```text
client direct upload to object storage
-> upload complete event
-> processing workflow
-> fan-out jobs:
   - scan
   - transcode
   - thumbnails
   - metadata extraction
-> fan-in status aggregator
-> publish when required steps complete
```

### Queue Choice

- SQS/BullMQ for job queues
- Kafka if upload/processing events feed many systems
- workflow engine if state machine gets complex

### Key Patterns

- direct-to-object-storage upload
- signed URLs
- processing state machine
- fan-out/fan-in
- retry per processing step
- DLQ and manual repair
- CDN for final assets

---

## Problem 10: Multi-Tenant SaaS Audit Log System

### Scenario

Every important action across a SaaS product must be auditable, searchable, exportable, and tamper-resistant.

### Requirements

- high write volume
- tenant isolation
- immutable audit entries
- search and filtering
- export
- retention policy
- compliance-friendly

### Design

```text
services emit audit events
-> Kafka/SQS
-> audit writer
-> append-only Postgres/ClickHouse table
-> object storage archive
-> search projection
```

### Key Choices

- use append-only writes
- never update/delete audit records casually
- include actor, action, target, tenant, timestamp, request_id
- store raw event and normalized fields
- archive cold records
- tenant-filter every query

### Key Patterns

- outbox from source services
- immutable event storage
- search projection
- export jobs
- retention management
- tamper-evident hashes for high-compliance needs

---

# Technology Decision Tables

## Queue / Stream Selection

| Need | Recommended Starting Point |
|---|---|
| Simple Node.js background jobs | BullMQ |
| AWS-managed durable async jobs | SQS |
| Routing with exchanges/topics | RabbitMQ |
| Durable event stream and replay | Kafka |
| Serverless fan-out | SNS + SQS/Lambda |
| Ordered per-key event processing | Kafka with good partition key |
| Scheduled/delayed jobs | BullMQ, SQS delay, or scheduler table |
| Multi-team event backbone | Kafka |
| Ephemeral live broadcast | Redis Pub/Sub |
| Moderate durable Redis-native events | Redis Streams |

## Database Selection

| Need | Recommended Starting Point |
|---|---|
| Strong transactions | Postgres |
| Flexible aggregate documents | MongoDB |
| High-scale key-value access | DynamoDB |
| Text search | Elasticsearch/OpenSearch |
| Semantic/vector search | pgvector, then dedicated vector DB if needed |
| Time-series metrics | TimescaleDB, ClickHouse, Prometheus depending use |
| Long-term analytics | BigQuery, Snowflake, Redshift, ClickHouse |
| Large files | Object storage |
| Relationship traversal | Graph DB only if traversal is core |

## Redis Feature Selection

| Need | Redis Feature |
|---|---|
| Cache object | String or hash |
| Counter | INCR |
| Unique membership | Set |
| Leaderboard | Sorted set |
| Sliding rate limit | Sorted set or token bucket |
| Simple queue | List |
| Job queue in Node.js | BullMQ |
| Durable-ish event stream | Redis Streams |
| Ephemeral broadcast | Pub/Sub |
| Approx unique count | HyperLogLog |
| Distributed lock | SET NX PX with caution, fencing for critical work |

---

# Practice Plan

## Weeks 1-2: Foundations and APIs

- [ ] Learn SLOs, p95/p99, throughput, bottlenecks
- [ ] Practice capacity estimates
- [ ] Compare REST, gRPC, WebSocket, SSE, webhook, polling
- [ ] Design idempotent API contracts

## Weeks 3-4: Databases and Consistency

- [ ] Study Postgres transaction/isolation basics
- [ ] Study MongoDB document modeling and sharding
- [ ] Study DynamoDB access-pattern modeling
- [ ] Study Elasticsearch as search projection
- [ ] Learn CAP and consistency models

## Weeks 5-6: Redis and Caching

- [ ] Learn cache-aside and invalidation
- [ ] Learn Redis data structures
- [ ] Design rate limiter
- [ ] Design leaderboard
- [ ] Compare Redis lists, streams, pub/sub, and BullMQ

## Weeks 7-8: Queues and Jobs

- [ ] Learn ACK/NACK, visibility timeout, DLQ
- [ ] Compare SQS, RabbitMQ, BullMQ
- [ ] Design webhook retry system
- [ ] Design background media processing pipeline
- [ ] Implement idempotent worker logic

## Weeks 9-10: Kafka and Streaming

- [ ] Learn topics, partitions, offsets, consumer groups
- [ ] Learn per-key ordering
- [ ] Learn replay and retention
- [ ] Design event analytics pipeline
- [ ] Design retry and DLQ topics

## Weeks 11-12: Fan-In, Fan-Out, Scaling

- [ ] Design notification fan-out
- [ ] Design video processing fan-in
- [ ] Design WebSocket rooms and broadcasting
- [ ] Design presence with TTL and heartbeats
- [ ] Design reconnect/resume for missed messages
- [ ] Learn hot partition detection
- [ ] Learn backpressure patterns
- [ ] Design partition keys for multiple systems

## Weeks 13-14: Reliability and Operations

- [ ] Learn outbox and inbox patterns
- [ ] Learn sagas
- [ ] Design reconciliation jobs
- [ ] Define metrics and alerts
- [ ] Write runbooks

## Weeks 15-16: Modern Design Problems

- [ ] Design AI document ingestion platform
- [ ] Design payment reconciliation system
- [ ] Design real-time collaboration backend
- [ ] Design workflow engine
- [ ] Design fraud/risk pipeline

---

# Final Master Checklist

## Foundations

- [ ] I can gather requirements
- [ ] I can estimate scale
- [ ] I can identify bottlenecks
- [ ] I can define SLOs
- [ ] I can reason about p95 and p99 latency

## Databases

- [ ] I can choose between Postgres, MongoDB, DynamoDB, Elasticsearch, Redis, and object storage
- [ ] I can model access patterns
- [ ] I understand indexes and query patterns
- [ ] I understand source-of-truth vs projection
- [ ] I understand consistency requirements per operation

## Queues and Streams

- [ ] I understand ACK/NACK
- [ ] I understand visibility timeout
- [ ] I understand retries and DLQs
- [ ] I understand idempotent consumers
- [ ] I understand Kafka topics, partitions, offsets, and consumer groups
- [ ] I can choose between queue and stream

## Redis

- [ ] I can design cache-aside
- [ ] I can avoid cache stampede
- [ ] I can use Redis sorted sets
- [ ] I can use Redis streams conceptually
- [ ] I understand BullMQ tradeoffs
- [ ] I understand Redis Pub/Sub limitations

## Sockets and Real-Time

- [ ] I can choose between WebSocket, SSE, polling, and webhook
- [ ] I can design rooms/channels
- [ ] I can design one-to-one, room, tenant, and global broadcasts
- [ ] I can design presence with TTL and heartbeats
- [ ] I can design reconnect/resume with last seen event IDs
- [ ] I understand ACKs, sequence numbers, and delivery guarantees
- [ ] I can scale sockets across multiple gateway nodes
- [ ] I can use Redis Pub/Sub safely for ephemeral cross-node broadcast
- [ ] I can handle slow clients and socket backpressure
- [ ] I can secure socket authentication and room authorization

## Distributed Systems

- [ ] I understand CAP
- [ ] I understand eventual consistency
- [ ] I understand replication tradeoffs
- [ ] I understand partitioning
- [ ] I understand hot keys and hot partitions
- [ ] I can design backpressure

## Reliability

- [ ] I can design idempotency keys
- [ ] I can use outbox pattern
- [ ] I can use inbox pattern
- [ ] I can design sagas
- [ ] I can design reconciliation jobs
- [ ] I can design graceful degradation

## Operations

- [ ] I can define useful metrics
- [ ] I can define alerts
- [ ] I can monitor queue depth and lag
- [ ] I can monitor DB health
- [ ] I can write runbooks
- [ ] I can plan replay and recovery

---

# Free Resource Index

## Foundations and Reliability

- [Google SRE Book](https://sre.google/sre-book/table-of-contents/)
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/)
- [Grafana Documentation](https://grafana.com/docs/)

## Databases

- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)
- [MongoDB Manual](https://www.mongodb.com/docs/manual/)
- [DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
- [Elasticsearch Guide](https://www.elastic.co/guide/index.html)
- [Redis Documentation](https://redis.io/docs/latest/)

## Messaging and Streaming

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Confluent Kafka Consumer Design](https://docs.confluent.io/kafka/design/consumer-design.html)
- [RabbitMQ Tutorials](https://www.rabbitmq.com/tutorials)
- [Amazon SQS Developer Guide](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)
- [Amazon SNS Developer Guide](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
- [Amazon Kinesis Data Streams](https://docs.aws.amazon.com/streams/latest/dev/introduction.html)
- [BullMQ Documentation](https://docs.bullmq.io/)

## Distributed Systems Theory

- [Perspectives on the CAP Theorem](https://groups.csail.mit.edu/tds/papers/Gilbert/Brewer2.pdf)
- [DynamoDB Read Consistency](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html)
- [MongoDB Read Concern](https://www.mongodb.com/docs/manual/reference/read-concern/)
- [MongoDB Write Concern](https://www.mongodb.com/docs/manual/reference/write-concern/)

---

# North-Star Mental Model

System design is the art of making tradeoffs explicit.

The best backend engineers do not say:

```text
Use Kafka.
Use Redis.
Use microservices.
Use DynamoDB.
```

They say:

```text
Given these consistency needs,
these access patterns,
this fan-out,
this failure model,
this latency target,
and this operational budget,
this is the simplest design that survives reality.
```

That is the level to aim for.
