# DBMS and Query Mastery Roadmap for Backend Developers

A deep, inductive roadmap for mastering DBMS concepts, SQL queries, MongoDB, and Cassandra as a backend developer.

This is not a shallow "learn SELECT, then JOIN" checklist. It starts from real backend questions, then derives data modeling, query design, indexes, transactions, query plans, consistency, and NoSQL tradeoffs.

No books. No videos. No paid-first resources. Only free/official reading and practice sources.

---

## Guiding Principle

Learn databases from questions.

Do not start with:

```text
What is a B-tree?
What is normalization?
What is aggregation?
What is a partition key?
```

Start with:

```text
What question does the product need answered quickly and correctly?
```

Then derive:

```text
question
-> data shape
-> write pattern
-> read pattern
-> consistency need
-> schema/model
-> indexes/partition keys
-> query
-> query plan
-> failure/performance limits
```

That is the inductive path.

---

## What You Should Be Able To Do After This

You should be able to:

- write strong SQL for backend and analytics use cases
- design relational schemas with constraints
- reason about joins, indexes, query plans, and transactions
- debug slow queries using `EXPLAIN`
- understand isolation levels and locking
- avoid ORM-generated query disasters
- design MongoDB collections around document access patterns
- write MongoDB queries and aggregation pipelines
- design Cassandra tables around query patterns
- choose partition keys and clustering columns
- understand NoSQL consistency tradeoffs
- know when SQL is better than NoSQL and when NoSQL earns its place

---

## Inductive Learning Spine

Use this path problem-first.

| Step | Product Question | Pain You Discover | Concept You Earn |
|---|---|---|---|
| 1 | Show a user's latest orders | need filtered sorted reads | `WHERE`, `ORDER BY`, indexes |
| 2 | Show order details with customer and items | data is related | joins, foreign keys, normalization |
| 3 | Show dashboard totals | need grouped summaries | aggregates, `GROUP BY`, `HAVING` |
| 4 | Show rank/change over time | grouped summary is not enough | window functions |
| 5 | Make the query fast | table scan hurts | indexes, query plans |
| 6 | Prevent bad data | app validation is not enough | constraints, transactions |
| 7 | Handle concurrent checkout | race conditions appear | isolation, locks, optimistic concurrency |
| 8 | Build search/filter UI | flexible query patterns appear | compound indexes, pagination |
| 9 | Store flexible product attributes | relational model gets awkward | JSONB or document modeling |
| 10 | Push Postgres beyond basic SQL | backend features need stronger DB tools | JSONB, FTS, partitioning, materialized views, locks |
| 11 | Query nested order documents | document read shape matters | MongoDB modeling and aggregation |
| 12 | Handle huge write-heavy event logs | relational joins no longer matter | Cassandra query-first modeling |
| 13 | Scale and operate | failures and growth appear | replication, sharding, backups, observability |

For each step, write:

```text
Question:
Naive schema/model:
Naive query:
What breaks:
Better model:
Better query:
Index/partition key:
Correctness risk:
Performance risk:
```

---

# Level 0: DBMS Mental Model

## Goal

Understand what a database is doing for you besides storing bytes.

## Core DBMS Responsibilities

| Responsibility | Meaning |
|---|---|
| Storage | Persist data on disk |
| Query execution | Find and transform data |
| Indexing | Avoid scanning everything |
| Transactions | Group operations safely |
| Concurrency control | Handle simultaneous users |
| Recovery | Survive crashes |
| Replication | Copy data to other nodes |
| Security | Control access |
| Optimization | Choose efficient execution plans |

## Backend Mental Model

When your API asks for data:

```text
API request
-> database connection
-> SQL/query parser
-> planner/optimizer
-> executor
-> indexes/table storage
-> rows/documents returned
-> API response
```

Your job is not just to write a query that returns correct data.

Your job is to write a query that returns correct data:

- fast enough
- under concurrency
- with predictable indexes
- without corrupting invariants
- without exploding memory or locks
- with safe failure behavior

## Tracker

- [ ] I understand what a DBMS does
- [ ] I understand query parsing, planning, and execution at a high level
- [ ] I understand why indexes exist
- [ ] I understand why transactions exist
- [ ] I understand why query shape matters

---

# Level 1: Basic SQL From Product Questions

## Goal

Learn SQL as a way to answer product questions, not as syntax trivia.

## Starting Schema

Use a simple commerce schema:

```sql
users(id, email, name, created_at)
orders(id, user_id, status, total_amount, created_at)
order_items(id, order_id, product_id, quantity, unit_price)
products(id, name, category, price, active)
payments(id, order_id, provider, status, amount, created_at)
```

## Product Question 1: Show a User's Latest Orders

Question:

```text
For this user, show the 20 newest orders.
```

Query:

```sql
SELECT id, status, total_amount, created_at
FROM orders
WHERE user_id = $1
ORDER BY created_at DESC
LIMIT 20;
```

Index you eventually need:

```sql
CREATE INDEX idx_orders_user_created
ON orders (user_id, created_at DESC);
```

What this teaches:

- `SELECT`
- `WHERE`
- `ORDER BY`
- `LIMIT`
- compound indexes
- access pattern thinking

## Product Question 2: Find Failed Payments

```sql
SELECT id, order_id, provider, amount, created_at
FROM payments
WHERE status = 'failed'
ORDER BY created_at DESC
LIMIT 100;
```

Think:

- Is `status = 'failed'` selective?
- How many failed rows exist?
- Should the index be `(status, created_at)`?
- Should old payment rows be archived?

## Product Question 3: Search Active Products in a Category

```sql
SELECT id, name, price
FROM products
WHERE active = true
  AND category = 'books'
ORDER BY price ASC
LIMIT 50;
```

Possible index:

```sql
CREATE INDEX idx_products_category_active_price
ON products (category, active, price);
```

## Basic SQL Concepts

| Concept | Use |
|---|---|
| `SELECT` | choose columns |
| `FROM` | choose table |
| `WHERE` | filter rows |
| `ORDER BY` | sort result |
| `LIMIT/OFFSET` | restrict result count |
| `DISTINCT` | remove duplicates |
| `CASE` | conditional values |
| `IN` | match list |
| `BETWEEN` | range filter |
| `LIKE/ILIKE` | pattern matching |
| `NULL` | missing/unknown value |

## Practice Drills

- Get all active products under a price.
- Get the latest 10 users.
- Get all orders for a status.
- Get all payments created today.
- Get products whose names contain a search term.
- Get users created between two dates.
- Return only the columns the API needs.

## Reading and Practice

- [SQLBolt](https://sqlbolt.com/)
- [PostgreSQL SQL Language](https://www.postgresql.org/docs/current/sql.html)
- [Mode SQL Tutorial](https://mode.com/sql-tutorial/)
- [PostgreSQL Exercises](https://pgexercises.com/)

## Tracker

- [ ] I can write `SELECT`, `WHERE`, `ORDER BY`, and `LIMIT`
- [ ] I can filter by dates, status, IDs, and booleans
- [ ] I can choose only needed columns
- [ ] I understand why query shape suggests indexes

---

# Level 2: Relationships, Joins, and Normalization

## Goal

Understand relational data and how joins reconstruct business objects.

## Inductive Problem

Product asks:

```text
Show an order page with:
- order status
- customer email
- payment status
- list of items
- product names
```

Naive idea:

```text
Store everything in one giant orders table.
```

What breaks:

- duplicated customer data
- duplicated product names
- update anomalies
- hard to enforce consistency
- huge rows
- awkward item lists

Now you earn relationships and normalization.

## Join Query

```sql
SELECT
  o.id AS order_id,
  o.status AS order_status,
  u.email,
  p.status AS payment_status,
  pr.name AS product_name,
  oi.quantity,
  oi.unit_price
FROM orders o
JOIN users u ON u.id = o.user_id
LEFT JOIN payments p ON p.order_id = o.id
JOIN order_items oi ON oi.order_id = o.id
JOIN products pr ON pr.id = oi.product_id
WHERE o.id = $1;
```

## Join Types

| Join | Meaning | Example |
|---|---|---|
| `INNER JOIN` | only matching rows | order with user |
| `LEFT JOIN` | keep left row even without match | order even if payment missing |
| `RIGHT JOIN` | keep right rows | less common in backend queries |
| `FULL OUTER JOIN` | keep unmatched from both sides | reconciliation reports |
| `CROSS JOIN` | all combinations | rare, can explode |
| self join | table joins itself | manager/employee, referral tree |

## Normalization

Normalization reduces duplication and prevents update anomalies.

| Form | Practical Meaning |
|---|---|
| 1NF | values are atomic; no repeated groups |
| 2NF | non-key fields depend on whole key |
| 3NF | fields depend on key, not other non-key fields |

Backend-friendly rule:

```text
Normalize source-of-truth transactional data.
Denormalize read models when performance or access patterns demand it.
```

## Foreign Keys

Foreign keys enforce relationships:

```sql
ALTER TABLE orders
ADD CONSTRAINT fk_orders_user
FOREIGN KEY (user_id) REFERENCES users(id);
```

Use them when correctness matters.

Be thoughtful with:

- cascading deletes
- high-write systems
- cross-service boundaries
- bulk loads

## Practice Drills

- Return order details with customer and items.
- Return users who have never ordered.
- Return products that have never sold.
- Return orders without successful payments.
- Return customers with more than 5 orders.
- Return pairs of users referred by the same referrer.

## Reading and Practice

- [PostgreSQL Table Expressions](https://www.postgresql.org/docs/current/queries-table-expressions.html)
- [Mode SQL Joins](https://mode.com/sql-tutorial/sql-joins/)
- [PostgreSQL Exercises: Joins and Subqueries](https://pgexercises.com/)

## Tracker

- [ ] I understand inner and outer joins
- [ ] I can write multi-table joins
- [ ] I understand foreign keys
- [ ] I understand normalization
- [ ] I know when denormalization is useful

---

# Level 3: Aggregation and Backend Analytics

## Goal

Answer summary questions.

## Inductive Problem

Product asks:

```text
Show admin dashboard:
- revenue today
- orders by status
- top products
- average order value
- repeat customers
```

Row-by-row fetching is wasteful.

Now you earn aggregation.

## Common Aggregate Queries

Revenue by day:

```sql
SELECT
  DATE(created_at) AS day,
  SUM(total_amount) AS revenue
FROM orders
WHERE status = 'paid'
GROUP BY DATE(created_at)
ORDER BY day DESC;
```

Orders by status:

```sql
SELECT status, COUNT(*) AS count
FROM orders
GROUP BY status
ORDER BY count DESC;
```

Top products:

```sql
SELECT
  p.id,
  p.name,
  SUM(oi.quantity) AS units_sold
FROM order_items oi
JOIN products p ON p.id = oi.product_id
GROUP BY p.id, p.name
ORDER BY units_sold DESC
LIMIT 10;
```

Repeat customers:

```sql
SELECT user_id, COUNT(*) AS order_count
FROM orders
GROUP BY user_id
HAVING COUNT(*) > 1;
```

## Concepts

| Concept | Use |
|---|---|
| `COUNT` | count rows |
| `SUM` | total numeric values |
| `AVG` | average |
| `MIN/MAX` | range |
| `GROUP BY` | group rows |
| `HAVING` | filter groups |
| conditional aggregate | count/sum only matching rows |

Conditional aggregation:

```sql
SELECT
  COUNT(*) AS total_orders,
  COUNT(*) FILTER (WHERE status = 'paid') AS paid_orders,
  COUNT(*) FILTER (WHERE status = 'failed') AS failed_orders
FROM orders;
```

## Practice Drills

- Revenue per day for last 30 days.
- Orders per status.
- Average order value per customer.
- Top categories by revenue.
- Customers with no orders.
- Products with high views but low purchases.
- Payment success rate by provider.

## Performance Warning

Aggregation over huge transactional tables can become expensive.

Options:

- add useful indexes
- precompute daily summaries
- use materialized views
- stream events to analytics storage
- move heavy analytics away from OLTP database

## Tracker

- [ ] I can use `GROUP BY`
- [ ] I can use `HAVING`
- [ ] I can write conditional aggregates
- [ ] I understand when aggregation becomes too expensive
- [ ] I can decide when to precompute summaries

---

# Level 4: Advanced SQL for Real Backend Work

## Goal

Write queries that express complex backend logic clearly.

## Subqueries

Find users who have placed orders:

```sql
SELECT id, email
FROM users
WHERE id IN (
  SELECT user_id
  FROM orders
);
```

Find users without orders:

```sql
SELECT u.id, u.email
FROM users u
WHERE NOT EXISTS (
  SELECT 1
  FROM orders o
  WHERE o.user_id = u.id
);
```

Prefer `EXISTS` when checking existence, especially when duplicates do not matter.

## CTEs

Use CTEs to make multi-step queries readable:

```sql
WITH paid_orders AS (
  SELECT *
  FROM orders
  WHERE status = 'paid'
),
customer_revenue AS (
  SELECT user_id, SUM(total_amount) AS revenue
  FROM paid_orders
  GROUP BY user_id
)
SELECT *
FROM customer_revenue
WHERE revenue > 10000;
```

## Window Functions

Inductive problem:

```text
Show each user's latest order.
```

Bad approach:

```text
Query once per user.
```

Better:

```sql
SELECT *
FROM (
  SELECT
    o.*,
    ROW_NUMBER() OVER (
      PARTITION BY user_id
      ORDER BY created_at DESC
    ) AS rn
  FROM orders o
) ranked
WHERE rn = 1;
```

Useful window functions:

| Function | Use |
|---|---|
| `ROW_NUMBER` | pick top row per group |
| `RANK` | ranking with ties |
| `DENSE_RANK` | ranking without gaps |
| `LAG` | previous row |
| `LEAD` | next row |
| running `SUM` | cumulative totals |
| moving `AVG` | rolling metrics |

## Recursive CTEs

Use for hierarchy traversal:

```sql
WITH RECURSIVE category_tree AS (
  SELECT id, parent_id, name, 0 AS depth
  FROM categories
  WHERE id = $1

  UNION ALL

  SELECT c.id, c.parent_id, c.name, ct.depth + 1
  FROM categories c
  JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT *
FROM category_tree;
```

## Upsert

Inductive problem:

```text
Create or update user's daily stats.
```

```sql
INSERT INTO user_daily_stats (user_id, day, login_count)
VALUES ($1, CURRENT_DATE, 1)
ON CONFLICT (user_id, day)
DO UPDATE SET login_count = user_daily_stats.login_count + 1;
```

## Practice Drills

- Latest order per user.
- Top 3 products per category.
- 7-day rolling revenue.
- Customers whose order amount increased from previous order.
- Referral tree for a user.
- Upsert daily login stats.
- Deduplicate rows keeping newest record.

## Reading and Practice

- [PostgreSQL SELECT](https://www.postgresql.org/docs/current/sql-select.html)
- [PostgreSQL Window Functions](https://www.postgresql.org/docs/current/tutorial-window.html)
- [Mode SQL Window Functions](https://mode.com/sql-tutorial/sql-window-functions/)
- [PostgreSQL Exercises](https://pgexercises.com/)

## Tracker

- [ ] I can write subqueries
- [ ] I can use `EXISTS`
- [ ] I can use CTEs
- [ ] I can use window functions
- [ ] I can write recursive CTEs for simple hierarchies
- [ ] I can use upserts safely

---

# Level 5: Indexes and Query Plans

## Goal

Understand why queries are slow and how databases decide execution strategies.

## Inductive Problem

This query is correct:

```sql
SELECT *
FROM orders
WHERE user_id = $1
ORDER BY created_at DESC
LIMIT 20;
```

It works with 10,000 rows.

It hurts with 100 million rows.

Now you earn indexes and query plans.

## Index Mental Model

An index is a separate data structure that helps the database find rows without scanning the whole table.

But indexes are not free:

- extra storage
- slower writes
- maintenance cost
- planner complexity
- potential bloat

## Common Index Types

| Index Type | Use |
|---|---|
| B-tree | equality, range, sorting, most default indexes |
| Hash | equality only in some systems |
| GIN | arrays, JSONB, full-text-ish structures in Postgres |
| GiST | geometric, ranges, specialized search |
| BRIN | very large naturally ordered tables |
| Full-text index | text search |
| Compound index | multi-column access pattern |
| Partial index | index subset of rows |
| Covering index | includes needed columns |

## Compound Index Order

For:

```sql
WHERE user_id = $1
ORDER BY created_at DESC
```

Good:

```sql
(user_id, created_at DESC)
```

Because:

```text
first filter to one user's rows
then already read in sorted order
```

Bad:

```sql
(created_at, user_id)
```

Usually worse for this query because it starts from time globally, not one user.

## Partial Index

If most products are inactive but you query active products:

```sql
CREATE INDEX idx_active_products_category_price
ON products (category, price)
WHERE active = true;
```

## Query Plan Practice

Use:

```sql
EXPLAIN ANALYZE
SELECT ...
```

Look for:

- sequential scan on large table
- index scan
- bitmap index scan
- nested loop
- hash join
- merge join
- sort step
- rows estimated vs actual rows
- buffers read
- total execution time

## Backend Query Smells

| Smell | Meaning |
|---|---|
| `SELECT *` | fetching unnecessary data |
| leading wildcard `LIKE '%term'` | often cannot use normal index |
| huge `OFFSET` | slow pagination |
| N+1 query pattern | ORM loads rows one-by-one |
| function on indexed column | may block index use |
| low-selectivity index | index may not help |
| many unused indexes | write overhead |
| unbounded query | API can accidentally fetch millions |

## Pagination

Offset pagination:

```sql
SELECT *
FROM orders
ORDER BY created_at DESC
LIMIT 20 OFFSET 100000;
```

Problem:

```text
database still walks/skips many rows
```

Keyset pagination:

```sql
SELECT *
FROM orders
WHERE created_at < $last_seen_created_at
ORDER BY created_at DESC
LIMIT 20;
```

Better for large scrolling feeds.

## Reading Resources

- [PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes.html)
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
- [SQLite Query Planner](https://www.sqlite.org/queryplanner.html)
- [SQLite EXPLAIN QUERY PLAN](https://sqlite.org/eqp.html)

## Tracker

- [ ] I understand B-tree indexes
- [ ] I can design compound indexes
- [ ] I understand partial indexes
- [ ] I can read basic `EXPLAIN ANALYZE`
- [ ] I understand keyset pagination
- [ ] I can identify N+1 query problems

---

# Level 6: Transactions, Isolation, and Concurrency

## Goal

Protect correctness when many users act at once.

## Inductive Problem

Two users buy the last item at the same time.

Naive flow:

```text
read inventory count = 1
both requests see 1
both create orders
both decrement inventory
inventory becomes invalid
```

Now you earn transactions and concurrency control.

## ACID

| Property | Meaning |
|---|---|
| Atomicity | all or nothing |
| Consistency | constraints/invariants preserved |
| Isolation | concurrent transactions do not break each other |
| Durability | committed data survives crash |

## Transaction Example

```sql
BEGIN;

UPDATE inventory
SET available = available - 1
WHERE product_id = $1
  AND available > 0;

-- check affected row count

INSERT INTO orders (user_id, status, total_amount)
VALUES ($2, 'created', $3);

COMMIT;
```

Key trick:

```text
Make the update conditional.
Do not only read then decide in application code.
```

## Isolation Levels

| Level | Allows | Use |
|---|---|---|
| Read Uncommitted | dirty reads in theory | rarely useful |
| Read Committed | each statement sees committed data | common default |
| Repeatable Read | transaction sees stable snapshot | reports, multi-step reads |
| Serializable | behaves like transactions ran one at a time | strongest correctness |

Practical rule:

```text
Use constraints, conditional updates, unique indexes, and row locks first.
Raise isolation when the business invariant truly needs it.
```

## Locks

Row lock:

```sql
SELECT *
FROM inventory
WHERE product_id = $1
FOR UPDATE;
```

Use when:

- you must read and then update same row
- business logic cannot be expressed as one conditional update

Be careful:

- long transactions hold locks
- lock ordering can cause deadlocks
- user interaction inside transaction is dangerous

## Optimistic Concurrency

Add a version column:

```sql
UPDATE documents
SET content = $new_content,
    version = version + 1
WHERE id = $id
  AND version = $expected_version;
```

If zero rows updated:

```text
someone else modified it
retry or show conflict
```

## Idempotency With Unique Constraints

Payment request:

```sql
CREATE UNIQUE INDEX idx_payments_idempotency
ON payments (idempotency_key);
```

Then retry-safe insert:

```sql
INSERT INTO payments (idempotency_key, order_id, amount, status)
VALUES ($1, $2, $3, 'pending')
ON CONFLICT (idempotency_key)
DO NOTHING;
```

## Reading Resources

- [PostgreSQL Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [PostgreSQL Concurrency Control](https://www.postgresql.org/docs/current/mvcc.html)
- [MySQL InnoDB Transaction Model](https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-model.html)

## Tracker

- [ ] I understand ACID
- [ ] I can design conditional updates
- [ ] I understand isolation levels
- [ ] I can use row locks carefully
- [ ] I understand optimistic concurrency
- [ ] I can use unique constraints for idempotency

---

# Level 7: Schema Design, Constraints, and Migrations

## Goal

Design schemas that preserve correctness and evolve safely.

## Inductive Problem

App-level validation says email must be unique.

Two requests arrive at the same time.

Both pass validation.

Both insert same email.

Now you earn database constraints.

## Constraints

| Constraint | Use |
|---|---|
| `PRIMARY KEY` | unique row identity |
| `FOREIGN KEY` | relationship integrity |
| `UNIQUE` | prevent duplicates |
| `NOT NULL` | required value |
| `CHECK` | business rule on value |
| exclusion constraint | prevent overlapping ranges in Postgres |

Example:

```sql
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

Check constraint:

```sql
ALTER TABLE orders
ADD CONSTRAINT valid_total_amount
CHECK (total_amount >= 0);
```

## Schema Evolution

Safe migration pattern:

```text
1. add nullable column
2. deploy app writing both old and new shape
3. backfill in batches
4. deploy app reading new shape
5. add NOT NULL/constraint
6. remove old column later
```

Avoid:

- huge blocking migrations
- rewriting massive tables during peak traffic
- adding non-null columns with defaults without understanding database behavior
- dropping columns immediately after deploy

## Soft Delete

```sql
deleted_at TIMESTAMPTZ
```

Pros:

- recovery
- audit
- historical queries

Cons:

- every query needs filter
- uniqueness gets tricky
- table grows forever

Partial unique index for active records:

```sql
CREATE UNIQUE INDEX unique_active_email
ON users (email)
WHERE deleted_at IS NULL;
```

## Tracker

- [ ] I can design primary keys
- [ ] I can use unique constraints
- [ ] I can use check constraints
- [ ] I understand foreign keys
- [ ] I can plan safe migrations
- [ ] I understand soft-delete tradeoffs

---

# Level 8: Backend Query Performance Patterns

## Goal

Avoid database performance traps common in backend applications.

## N+1 Queries

Bad:

```text
SELECT orders
for each order:
  SELECT user
```

Better:

```sql
SELECT o.*, u.email
FROM orders o
JOIN users u ON u.id = o.user_id
WHERE o.created_at >= now() - interval '1 day';
```

Or batch:

```sql
SELECT *
FROM users
WHERE id = ANY($user_ids);
```

## API Query Boundaries

Every list endpoint should define:

- max page size
- default sort
- allowed filters
- timeout
- index support
- stable pagination cursor

## Count Queries

`COUNT(*)` on huge filtered data can be expensive.

Options:

- exact count only when necessary
- approximate count for UI
- cached counters
- precomputed summaries
- avoid showing total pages for huge datasets

## Search Queries

Normal B-tree indexes do not solve every search.

Use:

- trigram indexes for fuzzy-ish text in Postgres
- full-text search for moderate text search
- Elasticsearch/OpenSearch for serious search relevance/facets
- MongoDB text indexes or Atlas Search where appropriate

## Reporting Queries

Do not let heavy admin reports crush OLTP traffic.

Options:

- read replica
- materialized views
- nightly summary tables
- event pipeline to analytics store
- export jobs

## Practice Drills

- Fix an N+1 query.
- Convert offset pagination to keyset pagination.
- Add indexes for a filter/sort endpoint.
- Rewrite a count-heavy endpoint.
- Design a report query that does not overload OLTP.
- Create a materialized summary table.

## Tracker

- [ ] I can identify N+1 queries
- [ ] I can design bounded list endpoints
- [ ] I understand count query costs
- [ ] I can choose search strategy
- [ ] I can separate OLTP and reporting workloads

---

# Level 9: MongoDB Query and Data Modeling

# Level 9: PostgreSQL Deep Dive for Backend Developers

## Goal

Learn PostgreSQL as a serious backend database, not just "SQL storage."

Postgres is often the best default database for backend systems because it gives you:

- strong SQL
- transactions
- constraints
- rich indexes
- JSONB
- full-text search
- materialized views
- partitioning
- extensions
- robust concurrency
- strong operational tooling

The inductive path is:

```text
backend feature
-> relational model
-> query
-> constraint
-> index
-> transaction behavior
-> operational concern
```

---

## Postgres Data Types You Should Know

| Type | Use |
|---|---|
| `BIGSERIAL` / identity | auto-incrementing IDs |
| `UUID` | public-safe/random IDs |
| `TEXT` | strings |
| `BOOLEAN` | flags |
| `NUMERIC` | money/precise decimal values |
| `INTEGER` / `BIGINT` | counts and IDs |
| `TIMESTAMPTZ` | timestamps with timezone awareness |
| `DATE` | calendar date |
| `JSONB` | semi-structured data |
| `ARRAY` | small bounded lists |
| `ENUM` | constrained status values, with migration caution |
| `INET` | IP addresses |
| range types | bookings, time ranges, price ranges |

## Money Warning

Use:

```sql
amount_cents BIGINT
```

or:

```sql
amount NUMERIC(12, 2)
```

Avoid floating point for money:

```sql
amount FLOAT
```

Floating point introduces rounding surprises.

---

## UUID vs Integer IDs

Integer IDs:

- compact
- index-friendly
- simple
- reveal approximate sequence/order

UUIDs:

- safer to expose publicly
- easier for distributed creation
- larger indexes
- random UUIDs can hurt index locality

Common backend pattern:

```text
internal numeric primary key
public UUID/external_id
```

Example:

```sql
CREATE TABLE orders (
  id BIGSERIAL PRIMARY KEY,
  public_id UUID NOT NULL UNIQUE,
  user_id BIGINT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

---

## Constraints as Backend Safety Nets

Postgres should enforce important invariants.

Unique idempotency key:

```sql
CREATE UNIQUE INDEX unique_payment_idempotency
ON payments (idempotency_key);
```

Valid status:

```sql
ALTER TABLE orders
ADD CONSTRAINT valid_order_status
CHECK (status IN ('created', 'paid', 'cancelled', 'refunded'));
```

Non-negative balance:

```sql
ALTER TABLE accounts
ADD CONSTRAINT non_negative_balance
CHECK (balance_cents >= 0);
```

No overlapping bookings:

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE TABLE room_bookings (
  room_id BIGINT NOT NULL,
  booking_range TSRANGE NOT NULL,
  EXCLUDE USING gist (
    room_id WITH =,
    booking_range WITH &&
  )
);
```

That exclusion constraint prevents overlapping time ranges for the same room.

---

## Postgres Index Types

| Index | Use |
|---|---|
| B-tree | default, equality/range/sort |
| GIN | JSONB, arrays, full-text search |
| GiST | ranges, geometric data, exclusion constraints |
| BRIN | huge append-only/time-ordered tables |
| Hash | equality, less commonly needed |

## B-tree Index

Most common:

```sql
CREATE INDEX idx_orders_user_created
ON orders (user_id, created_at DESC);
```

Good for:

```sql
WHERE user_id = ?
ORDER BY created_at DESC
```

## Partial Index

For unread notifications:

```sql
CREATE INDEX idx_notifications_unread
ON notifications (user_id, created_at DESC)
WHERE read_at IS NULL;
```

This is better than indexing every notification if unread queries are common and most rows are read.

## Covering Index

```sql
CREATE INDEX idx_orders_user_created_include_status
ON orders (user_id, created_at DESC)
INCLUDE (status, total_amount);
```

This can let Postgres answer a query from the index without visiting the table, depending on visibility.

## GIN Index for JSONB

```sql
CREATE INDEX idx_products_attributes_gin
ON products USING GIN (attributes);
```

Query:

```sql
SELECT *
FROM products
WHERE attributes @> '{"color": "black"}';
```

## BRIN Index for Large Append-Only Tables

Audit logs:

```sql
CREATE INDEX idx_audit_logs_created_brin
ON audit_logs USING BRIN (created_at);
```

BRIN can be useful when:

- table is huge
- data is naturally ordered by time
- approximate page ranges are enough

---

## JSONB in Postgres

Postgres can handle semi-structured data with JSONB.

Good use cases:

- flexible product attributes
- provider webhook payloads
- metadata fields
- feature flags/config blobs
- audit event raw payloads

Bad use cases:

- replacing every relational table
- fields that need frequent joins
- fields that need strong constraints
- unbounded deeply nested documents

Example:

```sql
CREATE TABLE products (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  attributes JSONB NOT NULL DEFAULT '{}'
);
```

Query JSONB:

```sql
SELECT *
FROM products
WHERE attributes ->> 'color' = 'black';
```

Containment query:

```sql
SELECT *
FROM products
WHERE attributes @> '{"waterproof": true}';
```

Hybrid modeling rule:

```text
Put stable, commonly filtered, relational fields in columns.
Put flexible, category-specific attributes in JSONB.
```

Good:

```text
category, price, active -> columns
shoe_size, battery_mah, isbn -> JSONB if category-specific
```

---

## Full-Text Search in Postgres

Postgres full-text search can be enough before adding Elasticsearch.

Example:

```sql
ALTER TABLE products
ADD COLUMN search_vector tsvector;

UPDATE products
SET search_vector =
  to_tsvector('english', coalesce(name, '') || ' ' || coalesce(description, ''));

CREATE INDEX idx_products_search
ON products USING GIN (search_vector);
```

Query:

```sql
SELECT id, name
FROM products
WHERE search_vector @@ plainto_tsquery('english', 'running shoes')
ORDER BY ts_rank(search_vector, plainto_tsquery('english', 'running shoes')) DESC;
```

Use Postgres FTS when:

- search is moderate
- relevance needs are simple
- operational simplicity matters

Use Elasticsearch/OpenSearch when:

- advanced relevance ranking matters
- faceting/filtering at scale matters
- typo tolerance/autocomplete is important
- search team needs dedicated search tooling

---

## Materialized Views

Inductive problem:

```text
Dashboard revenue query scans millions of orders every time.
```

Materialized view:

```sql
CREATE MATERIALIZED VIEW daily_revenue AS
SELECT
  DATE(created_at) AS day,
  SUM(total_amount) AS revenue
FROM orders
WHERE status = 'paid'
GROUP BY DATE(created_at);
```

Refresh:

```sql
REFRESH MATERIALIZED VIEW daily_revenue;
```

Concurrent refresh requires unique index:

```sql
CREATE UNIQUE INDEX idx_daily_revenue_day
ON daily_revenue (day);

REFRESH MATERIALIZED VIEW CONCURRENTLY daily_revenue;
```

Use materialized views when:

- query is expensive
- slightly stale data is acceptable
- refresh schedule is controllable

Avoid when:

- data must be real-time
- refresh cost is too high
- incremental updates are better

---

## Partitioning in Postgres

Partitioning splits one logical table into smaller physical pieces.

Common for:

- audit logs
- events
- time-series data
- multi-tenant data
- huge append-only tables

Time partition:

```sql
CREATE TABLE audit_logs (
  id BIGSERIAL,
  tenant_id BIGINT NOT NULL,
  action TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);
```

Monthly partition:

```sql
CREATE TABLE audit_logs_2026_05
PARTITION OF audit_logs
FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');
```

Benefits:

- faster deletes/drop old partitions
- smaller indexes per partition
- partition pruning
- easier archival

Risks:

- operational complexity
- bad partition key gives little benefit
- too many partitions cause overhead
- constraints/indexes need planning

---

## Transactions and Locks in Postgres

## Row-Level Locking

```sql
SELECT *
FROM orders
WHERE id = $1
FOR UPDATE;
```

This prevents another transaction from modifying the selected row until current transaction ends.

Use for:

- state transitions
- inventory reservation
- payment status update
- job claiming

## Skip Locked Job Queue Pattern

Postgres can act as a simple durable job queue at moderate scale.

```sql
WITH next_job AS (
  SELECT id
  FROM jobs
  WHERE status = 'pending'
  ORDER BY created_at
  FOR UPDATE SKIP LOCKED
  LIMIT 1
)
UPDATE jobs
SET status = 'processing',
    started_at = now()
WHERE id IN (SELECT id FROM next_job)
RETURNING *;
```

Use this when:

- job volume is moderate
- operational simplicity matters
- strong DB-backed state is useful

Move to a dedicated queue when:

- throughput is high
- delayed/retry semantics get complex
- workers need independent scaling
- DB becomes bottleneck

## Advisory Locks

Postgres advisory locks are application-defined locks.

Example:

```sql
SELECT pg_advisory_lock(12345);
SELECT pg_advisory_unlock(12345);
```

Use carefully for:

- one-at-a-time scheduled jobs
- coarse-grained coordination
- migration guards

Avoid for:

- replacing proper constraints
- long user-facing operations
- unclear lock key schemes

---

## Isolation in Postgres

Postgres default is `READ COMMITTED`.

Practical implications:

```text
Each statement sees a snapshot of committed data at statement start.
Two statements in same transaction can see different committed data.
```

Use `REPEATABLE READ` when:

- multi-query report needs stable snapshot
- you do not want data changing mid-transaction view

Use `SERIALIZABLE` when:

- correctness demands serial behavior
- you can handle retrying serialization failures

Important:

```text
Serializable transactions may fail and need retry logic.
```

---

## Postgres Upsert Patterns

Create-or-ignore:

```sql
INSERT INTO users (email, name)
VALUES ($1, $2)
ON CONFLICT (email) DO NOTHING;
```

Create-or-update:

```sql
INSERT INTO user_daily_stats (user_id, day, login_count)
VALUES ($1, CURRENT_DATE, 1)
ON CONFLICT (user_id, day)
DO UPDATE SET login_count = user_daily_stats.login_count + 1;
```

Idempotent event processing:

```sql
INSERT INTO processed_events (event_id, processed_at)
VALUES ($1, now())
ON CONFLICT (event_id) DO NOTHING;
```

Then only perform side effect if insert succeeded.

---

## Postgres for Multi-Tenancy

Common pattern:

```sql
tenant_id BIGINT NOT NULL
```

Composite indexes:

```sql
CREATE INDEX idx_orders_tenant_user_created
ON orders (tenant_id, user_id, created_at DESC);
```

Tenant-safe query:

```sql
SELECT *
FROM orders
WHERE tenant_id = $tenant_id
  AND user_id = $user_id;
```

Danger:

```sql
SELECT *
FROM orders
WHERE user_id = $user_id;
```

Missing tenant filter can leak data.

Postgres also has Row-Level Security, but it must be designed and tested carefully.

---

## Postgres Maintenance and Operations

## VACUUM

Postgres uses MVCC. Updates/deletes leave dead tuples that need cleanup.

Autovacuum usually handles this, but you must monitor it.

Watch for:

- table bloat
- dead tuples
- long-running transactions blocking cleanup
- transaction ID wraparound risk

## ANALYZE

Postgres uses statistics to plan queries.

If stats are stale, planner may choose bad plans.

Autovacuum also runs analyze, but bulk changes may require manual analyze.

```sql
ANALYZE orders;
```

## Connection Pooling

Too many DB connections can hurt Postgres.

Use a pooler/application pool.

Common issue:

```text
100 app instances * 50 connections = 5000 DB connections
```

Better:

```text
bounded pool size
PgBouncer if needed
read replicas where useful
```

## Slow Query Monitoring

Enable/log:

- slow query logs
- `pg_stat_statements`
- lock waits
- deadlocks
- connection saturation

Useful extension:

```sql
CREATE EXTENSION pg_stat_statements;
```

Track:

- total time
- mean time
- calls
- rows returned
- shared buffers hit/read

---

## Postgres Extensions Worth Knowing

| Extension | Use |
|---|---|
| `pg_stat_statements` | query performance stats |
| `pg_trgm` | trigram search/similarity |
| `btree_gist` | exclusion constraints with scalar values |
| `uuid-ossp` or built-in gen funcs | UUID generation |
| `pgcrypto` | cryptographic functions |
| `pgvector` | vector search for embeddings |
| PostGIS | geospatial data |

Trigram example:

```sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX idx_products_name_trgm
ON products USING GIN (name gin_trgm_ops);

SELECT *
FROM products
WHERE name ILIKE '%shoe%';
```

---

## Postgres Backend Patterns

## Pattern 1: Idempotent Payment Insert

```sql
CREATE UNIQUE INDEX unique_payment_provider_key
ON payments (provider, provider_payment_id);
```

Then:

```sql
INSERT INTO payments (...)
VALUES (...)
ON CONFLICT (provider, provider_payment_id)
DO UPDATE SET updated_at = now()
RETURNING *;
```

## Pattern 2: Outbox Table

```sql
CREATE TABLE outbox_events (
  id BIGSERIAL PRIMARY KEY,
  topic TEXT NOT NULL,
  payload JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  published_at TIMESTAMPTZ
);
```

Inside same transaction:

```sql
INSERT INTO orders (...);
INSERT INTO outbox_events (topic, payload) VALUES (...);
```

Publisher reads unpublished events and publishes to queue/Kafka.

## Pattern 3: Audit Log

```sql
CREATE TABLE audit_logs (
  id BIGSERIAL PRIMARY KEY,
  tenant_id BIGINT NOT NULL,
  actor_id BIGINT,
  action TEXT NOT NULL,
  target_type TEXT NOT NULL,
  target_id TEXT NOT NULL,
  payload JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

Index:

```sql
CREATE INDEX idx_audit_tenant_created
ON audit_logs (tenant_id, created_at DESC);
```

## Pattern 4: Soft Delete With Partial Unique Index

```sql
CREATE UNIQUE INDEX unique_active_user_email
ON users (email)
WHERE deleted_at IS NULL;
```

## Pattern 5: Keyset Pagination

```sql
SELECT *
FROM orders
WHERE user_id = $1
  AND (created_at, id) < ($last_created_at, $last_id)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

Index:

```sql
CREATE INDEX idx_orders_user_created_id
ON orders (user_id, created_at DESC, id DESC);
```

---

## Postgres Practice Drills

- [ ] Create schema with constraints for users, orders, payments.
- [ ] Add partial index for unread notifications.
- [ ] Add compound index for tenant/user/latest orders.
- [ ] Use `EXPLAIN ANALYZE` before and after index creation.
- [ ] Implement keyset pagination.
- [ ] Implement idempotent payment insert with `ON CONFLICT`.
- [ ] Implement safe inventory decrement.
- [ ] Implement job claiming with `FOR UPDATE SKIP LOCKED`.
- [ ] Implement audit log table with JSONB payload.
- [ ] Implement materialized daily revenue view.
- [ ] Implement JSONB product attributes and GIN index.
- [ ] Implement full-text search for products.
- [ ] Implement no-overlap booking constraint.
- [ ] Inspect slow queries with `pg_stat_statements`.

## Reading Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)
- [PostgreSQL Data Types](https://www.postgresql.org/docs/current/datatype.html)
- [PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes.html)
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
- [PostgreSQL JSON Types](https://www.postgresql.org/docs/current/datatype-json.html)
- [PostgreSQL Full Text Search](https://www.postgresql.org/docs/current/textsearch.html)
- [PostgreSQL Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [PostgreSQL Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html)
- [PostgreSQL Partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html)
- [PostgreSQL Materialized Views](https://www.postgresql.org/docs/current/rules-materializedviews.html)
- [PostgreSQL pg_stat_statements](https://www.postgresql.org/docs/current/pgstatstatements.html)

## Tracker

- [ ] I understand important Postgres data types
- [ ] I can design Postgres constraints
- [ ] I can choose B-tree, GIN, GiST, BRIN indexes
- [ ] I can use JSONB appropriately
- [ ] I can use Postgres full-text search
- [ ] I can use materialized views
- [ ] I understand partitioning basics
- [ ] I can use row locks and `SKIP LOCKED`
- [ ] I can design idempotent upserts
- [ ] I understand autovacuum and analyze at a high level
- [ ] I can use `pg_stat_statements` conceptually

---

# Level 10: MongoDB Query and Data Modeling

## Goal

Use MongoDB as a document database intentionally, not as "SQL but JSON."

## Inductive Problem

Product catalog has flexible attributes:

```text
Book: author, ISBN, pages
Phone: storage, battery, camera
Shoes: size, color, material
```

A rigid relational schema becomes awkward.

Now you earn document modeling.

## Document Mental Model

MongoDB stores documents:

```json
{
  "_id": "p1",
  "name": "Running Shoe",
  "category": "shoes",
  "price": 120,
  "attributes": {
    "size": 10,
    "color": "black",
    "material": "mesh"
  }
}
```

## Embed vs Reference

Embed when:

- child data is usually read with parent
- child data is bounded
- child lifecycle belongs to parent
- duplication is acceptable

Reference when:

- child is large or unbounded
- child is shared
- child changes independently
- many-to-many relationship exists

Example: order document can embed items:

```json
{
  "_id": "order1",
  "user_id": "u1",
  "status": "paid",
  "items": [
    { "product_id": "p1", "name": "Shoe", "quantity": 1, "price": 120 }
  ],
  "created_at": "2026-05-31T10:00:00Z"
}
```

Why embedding item snapshot is good:

```text
Order history should preserve product name/price at purchase time.
```

## MongoDB Queries

Find active products:

```javascript
db.products.find({
  active: true,
  category: "shoes"
}).sort({ price: 1 }).limit(50)
```

Find nested attribute:

```javascript
db.products.find({
  "attributes.color": "black"
})
```

Projection:

```javascript
db.products.find(
  { category: "shoes" },
  { name: 1, price: 1, _id: 0 }
)
```

Update:

```javascript
db.products.updateOne(
  { _id: "p1" },
  { $set: { price: 130 } }
)
```

Array update:

```javascript
db.orders.updateOne(
  { _id: "order1", "items.product_id": "p1" },
  { $set: { "items.$.quantity": 2 } }
)
```

## MongoDB Aggregation

Revenue by category:

```javascript
db.orders.aggregate([
  { $match: { status: "paid" } },
  { $unwind: "$items" },
  {
    $group: {
      _id: "$items.category",
      revenue: { $sum: { $multiply: ["$items.quantity", "$items.price"] } }
    }
  },
  { $sort: { revenue: -1 } }
])
```

Pipeline stages:

| Stage | Use |
|---|---|
| `$match` | filter |
| `$project` | reshape fields |
| `$group` | aggregate |
| `$sort` | sort |
| `$limit` | restrict |
| `$unwind` | explode array |
| `$lookup` | join-like lookup |
| `$facet` | multiple aggregations |

## MongoDB Indexes

Compound index:

```javascript
db.products.createIndex({ category: 1, active: 1, price: 1 })
```

Index nested field:

```javascript
db.products.createIndex({ "attributes.color": 1 })
```

Use explain:

```javascript
db.products.find({ category: "shoes" }).explain("executionStats")
```

## MongoDB Sharding

Shard key matters deeply.

Good shard key:

- appears in common queries
- high cardinality
- distributes writes
- avoids hot chunks

Bad shard key:

- low-cardinality status
- monotonically increasing timestamp alone
- field not used in queries
- tenant ID if one tenant can dominate

## MongoDB Anti-Patterns

- unbounded arrays inside documents
- using `$lookup` everywhere like SQL joins
- no indexes for common queries
- huge documents approaching limits
- choosing shard key after production pain
- modeling without access patterns
- using MongoDB only because frontend sends JSON

## Reading Resources

- [MongoDB Data Modeling](https://www.mongodb.com/docs/manual/data-modeling/)
- [MongoDB Query Documents](https://www.mongodb.com/docs/manual/tutorial/query-documents/)
- [MongoDB Aggregation](https://www.mongodb.com/docs/manual/aggregation/)
- [MongoDB Indexes](https://www.mongodb.com/docs/manual/indexes/)
- [MongoDB Query Optimization](https://www.mongodb.com/docs/manual/core/query-optimization/)
- [MongoDB Sharding](https://www.mongodb.com/docs/manual/sharding/)

## Practice Drills

- Model product catalog with flexible attributes.
- Model orders with embedded item snapshots.
- Query nested fields.
- Build aggregation for revenue by category.
- Add compound indexes for filter/sort queries.
- Use `explain` to compare indexed vs non-indexed query.
- Redesign an unbounded comments array into separate collection.

## Tracker

- [ ] I understand embedding vs referencing
- [ ] I can write MongoDB find queries
- [ ] I can write projections and updates
- [ ] I can write aggregation pipelines
- [ ] I can design MongoDB indexes
- [ ] I can explain shard key tradeoffs

---

# Level 11: Cassandra Query and Data Modeling

## Goal

Understand Cassandra as a query-first, distributed wide-column database.

## Inductive Problem

You need to store huge event streams:

```text
millions of device events per minute
query latest events for device
query events for device by day
high write availability matters
joins do not matter
```

Relational modeling starts to hurt.

Now you earn Cassandra.

## Cassandra Mental Model

Cassandra is built for:

- high write throughput
- horizontal scaling
- distributed availability
- query patterns known upfront
- denormalized tables
- reads by partition key

Cassandra is not built for:

- arbitrary joins
- ad-hoc queries
- relational constraints
- multi-row transactions like SQL
- scanning everything casually

## Query-First Rule

In SQL, you often model entities first, then query flexibly.

In Cassandra:

```text
Start with queries.
Create tables for those queries.
Duplicate data intentionally.
```

## Cassandra Primary Key

```sql
PRIMARY KEY ((partition_key), clustering_column)
```

Partition key:

```text
decides which node stores the data
```

Clustering columns:

```text
sort rows inside the partition
```

## Example: Device Events

Query:

```text
Get latest events for device on a given day.
```

Table:

```sql
CREATE TABLE device_events_by_day (
  device_id text,
  day date,
  event_time timestamp,
  event_id uuid,
  event_type text,
  payload text,
  PRIMARY KEY ((device_id, day), event_time, event_id)
) WITH CLUSTERING ORDER BY (event_time DESC);
```

Query:

```sql
SELECT *
FROM device_events_by_day
WHERE device_id = 'd1'
  AND day = '2026-05-31'
LIMIT 100;
```

Why this works:

```text
partition = device + day
within partition rows are sorted by event_time
query reads one bounded partition
```

## Bad Cassandra Query

```sql
SELECT *
FROM device_events_by_day
WHERE event_type = 'error';
```

Why bad:

```text
event_type is not the partition key
Cassandra cannot efficiently find this globally
```

Better:

Create another table for that query:

```sql
CREATE TABLE error_events_by_day (
  day date,
  event_time timestamp,
  device_id text,
  event_id uuid,
  payload text,
  PRIMARY KEY ((day), event_time, device_id, event_id)
) WITH CLUSTERING ORDER BY (event_time DESC);
```

## Cassandra Data Modeling Rules

| Rule | Meaning |
|---|---|
| Model around queries | each table serves a query |
| Minimize partitions read | ideally one partition per query |
| Spread data evenly | avoid hot partition keys |
| Keep partitions bounded | avoid infinitely growing partitions |
| Denormalize intentionally | duplicate data for reads |
| Avoid joins | Cassandra does not support relational joins |
| Avoid ad-hoc filters | filters should match primary key/index design |

## Partition Key Design

Bad:

```text
partition key = device_id
```

If one device sends endless events, partition grows forever.

Better:

```text
partition key = (device_id, day)
```

This buckets data by time.

But if one device is extremely hot:

```text
partition key = (device_id, day, bucket)
```

## Clustering Columns

Use clustering columns to support ordering within partition:

```sql
PRIMARY KEY ((user_id), created_at, notification_id)
```

Good for:

```text
latest notifications for user
```

## Consistency Levels

Cassandra lets you tune read/write consistency.

Common levels:

| Level | Meaning |
|---|---|
| ONE | one replica responds |
| QUORUM | majority of replicas respond |
| LOCAL_QUORUM | majority in local datacenter |
| ALL | all replicas respond |

Rule of thumb:

```text
Higher consistency = more coordination and latency.
Lower consistency = more availability and possible staleness.
```

## Lightweight Transactions

Cassandra has lightweight transactions for conditional updates, but they are expensive compared to normal writes.

Use sparingly for:

- uniqueness-like constraints
- compare-and-set
- rare coordination

Do not build every write path around LWT unless you accept the cost.

## TTL and Tombstones

Cassandra supports TTL:

```sql
INSERT INTO sessions (user_id, token, created_at)
VALUES ('u1', 'abc', toTimestamp(now()))
USING TTL 3600;
```

Expired/deleted data creates tombstones.

Too many tombstones can hurt reads.

Be careful with:

- frequent deletes
- wide partitions
- short TTL on massive data
- range scans over tombstone-heavy partitions

## Secondary Indexes

Secondary indexes exist, but they are not magic SQL indexes.

Be cautious when:

- high cardinality fields
- low selectivity
- large clusters
- high write rates

Cassandra modeling should mostly rely on primary-key-based query tables.

## Reading Resources

- [Apache Cassandra Data Modeling Introduction](https://cassandra.apache.org/doc/latest/cassandra/developing/data-modeling/intro.html)
- [Apache Cassandra CQL Data Definition](https://cassandra.apache.org/doc/3.11/cassandra/cql/ddl.html)
- [Apache Cassandra Secondary Indexes](https://cassandra.apache.org/doc/3.11/cassandra/cql/indexes.html)
- [DataStax Cassandra Data Modeling](https://www.datastax.com/dev/modeling)
- [DataStax Data Modeling Best Practices](https://docs.datastax.com/en/cql/hcd/data-modeling/best-practices.html)

## Practice Drills

- Model latest notifications by user.
- Model messages by conversation and day.
- Model device events by device/day.
- Model error events by day.
- Model user activity by tenant/day.
- Add bucket to avoid hot partitions.
- Explain which queries each table supports.
- Identify queries Cassandra should not serve.

## Tracker

- [ ] I understand partition keys
- [ ] I understand clustering columns
- [ ] I can model one Cassandra table per query
- [ ] I understand denormalization in Cassandra
- [ ] I understand consistency levels
- [ ] I understand TTL and tombstone risks
- [ ] I know why secondary indexes are limited

---

# Level 12: SQL vs MongoDB vs Cassandra

## Goal

Choose the right database based on the problem, not hype.

## Decision Table

| Requirement | SQL/Postgres | MongoDB | Cassandra |
|---|---|---|---|
| Strong transactions | excellent | decent for some cases | limited |
| Joins | excellent | limited via `$lookup` | no |
| Flexible documents | okay with JSONB | excellent | not primary strength |
| Ad-hoc queries | excellent | good with indexes | poor |
| High write scale | good up to a point | good with sharding | excellent |
| Query-first modeling | useful | useful | mandatory |
| Constraints | excellent | limited | weak |
| Event/time-series at huge scale | possible with partitioning | possible | strong |
| Operational simplicity | strong default | moderate | higher complexity |
| Data duplication | optional | common | required |

## Use SQL When

- correctness matters
- relationships matter
- transactions matter
- queries are evolving
- constraints are valuable
- team wants operational simplicity

## Use MongoDB When

- data is naturally document-shaped
- reads fetch aggregates
- schema varies significantly
- embedding reduces joins
- flexible product/entity attributes matter

## Use Cassandra When

- write throughput is huge
- availability across nodes matters
- query patterns are known
- data is naturally partitionable
- denormalized query tables are acceptable
- eventual/tunable consistency is acceptable

## Do Not Use Cassandra When

- you need joins
- you need ad-hoc filtering
- your query patterns change weekly
- you need strict relational constraints
- your dataset fits comfortably in Postgres
- your team cannot operate it

## Do Not Use MongoDB When

- relationships dominate
- multi-document invariants dominate
- you mainly need SQL joins
- you choose it only because JSON feels convenient

## Do Not Avoid SQL Too Early

Postgres can handle a lot.

Before leaving SQL, check:

- indexes
- query plans
- connection pooling
- read replicas
- partitioning
- caching
- materialized views
- async processing
- archiving old data

## Tracker

- [ ] I can choose SQL vs MongoDB vs Cassandra
- [ ] I can explain when SQL is the better default
- [ ] I can explain when document modeling helps
- [ ] I can explain when Cassandra earns its complexity

---

# Level 13: Replication, Sharding, Backups, and Operations

## Goal

Understand production database concerns.

## Replication

Replication copies data to other nodes.

Uses:

- high availability
- read scaling
- disaster recovery
- regional latency

Risks:

- replica lag
- stale reads
- failover complexity
- split brain
- consistency tradeoffs

## Sharding

Sharding splits data across nodes.

Shard key matters.

Bad shard key:

```text
status
```

Why:

```text
low cardinality, uneven distribution
```

Better shard key:

```text
tenant_id + hash bucket
user_id
device_id + day
```

Depending on access pattern.

## Backups

Backups are not real until restore is tested.

Backup checklist:

- [ ] automated backups
- [ ] point-in-time recovery if needed
- [ ] restore drill
- [ ] backup encryption
- [ ] retention policy
- [ ] cross-region copy if needed
- [ ] documented recovery steps

## Database Observability

Track:

- slow queries
- query throughput
- locks/deadlocks
- connection pool usage
- cache hit rate
- index usage
- replication lag
- disk usage
- CPU and memory
- compaction/vacuum health
- tombstones in Cassandra
- chunk distribution in MongoDB

## Tracker

- [ ] I understand replication
- [ ] I understand replica lag
- [ ] I understand sharding basics
- [ ] I can design shard keys
- [ ] I understand backup/restore requirements
- [ ] I can define database health metrics

---

# Comprehensive Practice Plan

## SQL Practice Track

Use one schema for most exercises:

```text
users
orders
order_items
products
payments
refunds
shipments
notifications
sessions
audit_logs
```

## Phase 1: Basic Queries

- [ ] latest users
- [ ] orders by status
- [ ] products by category
- [ ] payments by provider
- [ ] sessions active after timestamp
- [ ] notifications unread by user

## Phase 2: Joins

- [ ] order detail page
- [ ] customer order history
- [ ] orders with failed payments
- [ ] products never ordered
- [ ] users without sessions
- [ ] refunds with payment details

## Phase 3: Aggregations

- [ ] revenue per day
- [ ] revenue per category
- [ ] payment success rate by provider
- [ ] average order value by user cohort
- [ ] top products by quantity
- [ ] refund rate by category

## Phase 4: Window Functions

- [ ] latest order per user
- [ ] first purchase per user
- [ ] previous order amount
- [ ] 7-day rolling revenue
- [ ] top 3 products per category
- [ ] rank customers by monthly spend

## Phase 5: Performance

- [ ] add index for latest orders by user
- [ ] add index for unread notifications
- [ ] compare offset vs keyset pagination
- [ ] use `EXPLAIN ANALYZE`
- [ ] fix N+1 query
- [ ] build materialized daily revenue summary

## Phase 6: Transactions

- [ ] safe inventory decrement
- [ ] idempotent payment creation
- [ ] refund state transition
- [ ] optimistic document update
- [ ] duplicate webhook prevention
- [ ] concurrent seat booking

---

# MongoDB Practice Track

## Dataset Ideas

- product catalog
- orders with embedded item snapshots
- user profiles with preferences
- support tickets with messages
- IoT device metadata
- content documents with tags

## Drills

- [ ] model product attributes as documents
- [ ] embed bounded child documents
- [ ] reference unbounded child documents
- [ ] query nested fields
- [ ] update nested fields
- [ ] aggregate revenue from embedded items
- [ ] build compound index
- [ ] use `explain`
- [ ] redesign unbounded array
- [ ] choose shard key for tenant-heavy workload

---

# Cassandra Practice Track

## Query-First Modeling Drills

For each query, create a table.

## Query 1: Latest Notifications by User

```text
Get latest 50 notifications for user.
```

Think:

```text
partition key = user_id
clustering = created_at DESC
```

But ask:

```text
Can one user have millions of notifications?
Do we need day/month bucket?
```

## Query 2: Messages by Conversation and Day

```text
Get messages for conversation on a day.
```

Think:

```text
partition key = conversation_id + day
clustering = message_time
```

## Query 3: Device Events by Device and Hour

```text
Get events for device during hour.
```

Think:

```text
partition key = device_id + hour_bucket
clustering = event_time
```

## Query 4: Tenant Activity by Day

```text
Get activity events for tenant by day.
```

If tenant can be huge, add bucket:

```text
partition key = tenant_id + day + bucket
```

## Drills

- [ ] define query
- [ ] choose partition key
- [ ] choose clustering columns
- [ ] estimate partition size
- [ ] identify hot partition risk
- [ ] decide TTL
- [ ] decide consistency level
- [ ] explain unsupported queries

---

# Modern Backend DB Problems

## Problem 1: Payment Ledger

Need:

- correctness
- audit trail
- no double spend
- immutable entries

Use:

- SQL/Postgres
- transactions
- constraints
- idempotency keys

Avoid:

- MongoDB for convenience
- Redis as source of truth
- Cassandra unless you really know why

Practice:

- ledger_entries table
- double-entry constraint thinking
- balance query
- idempotent transaction insert

## Problem 2: Notification Inbox

Need:

- latest notifications by user
- unread count
- mark read
- high write rate

Options:

- Postgres for normal scale
- Cassandra for very high-scale inbox by user/time
- Redis for unread count cache

Practice:

- SQL schema and index
- Cassandra query table
- Redis unread count invalidation

## Problem 3: Product Catalog With Flexible Attributes

Need:

- category-specific fields
- filtering
- search
- admin edits

Options:

- Postgres JSONB for moderate flexibility
- MongoDB for document-heavy catalog
- Elasticsearch for search projection

Practice:

- MongoDB embedded attributes
- indexes on common filters
- search projection design

## Problem 4: Chat Messages

Need:

- messages by conversation
- pagination
- unread state
- search

Options:

- Postgres initially
- Cassandra for huge conversation/time write scale
- Elasticsearch/OpenSearch for message search

Practice:

- SQL keyset pagination
- Cassandra table by conversation/day
- unread counters

## Problem 5: Analytics Events

Need:

- huge writes
- time-range queries
- aggregations
- retention

Options:

- Kafka/Kinesis ingest
- Cassandra/ClickHouse/object storage depending access
- Postgres only for smaller scale or metadata

Practice:

- Cassandra event table
- daily aggregate SQL table
- raw event retention strategy

## Problem 6: Multi-Tenant Audit Logs

Need:

- append-only
- tenant isolation
- search
- export
- retention

Options:

- Postgres partitioned table
- Cassandra for huge tenant/time logs
- Elasticsearch/OpenSearch projection for search
- object storage archive

Practice:

- SQL partitioned audit logs
- Cassandra tenant/day table
- export query boundaries

---

# Free Resource Index

## SQL and Relational DBs

- [SQLBolt](https://sqlbolt.com/)
- [PostgreSQL Exercises](https://pgexercises.com/)
- [Mode SQL Tutorial](https://mode.com/sql-tutorial/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/)
- [PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes.html)
- [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
- [PostgreSQL Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [SQLite Query Planner](https://www.sqlite.org/queryplanner.html)
- [SQLite EXPLAIN QUERY PLAN](https://sqlite.org/eqp.html)
- [MySQL Documentation](https://dev.mysql.com/doc/)

## MongoDB

- [MongoDB Data Modeling](https://www.mongodb.com/docs/manual/data-modeling/)
- [MongoDB Query Documents](https://www.mongodb.com/docs/manual/tutorial/query-documents/)
- [MongoDB Aggregation](https://www.mongodb.com/docs/manual/aggregation/)
- [MongoDB Indexes](https://www.mongodb.com/docs/manual/indexes/)
- [MongoDB Query Optimization](https://www.mongodb.com/docs/manual/core/query-optimization/)
- [MongoDB Sharding](https://www.mongodb.com/docs/manual/sharding/)

## Cassandra

- [Apache Cassandra Data Modeling Introduction](https://cassandra.apache.org/doc/latest/cassandra/developing/data-modeling/intro.html)
- [Apache Cassandra CQL Data Definition](https://cassandra.apache.org/doc/3.11/cassandra/cql/ddl.html)
- [Apache Cassandra Secondary Indexes](https://cassandra.apache.org/doc/3.11/cassandra/cql/indexes.html)
- [DataStax Cassandra Data Modeling](https://www.datastax.com/dev/modeling)
- [DataStax Data Modeling Best Practices](https://docs.datastax.com/en/cql/hcd/data-modeling/best-practices.html)

---

# Final Master Checklist

## SQL

- [ ] I can write basic SELECT queries
- [ ] I can write joins
- [ ] I can use aggregations
- [ ] I can use subqueries and CTEs
- [ ] I can use window functions
- [ ] I can write upserts
- [ ] I can design constraints
- [ ] I can read query plans
- [ ] I can design indexes
- [ ] I can handle transactions and concurrency

## PostgreSQL

- [ ] I understand Postgres-specific data types
- [ ] I can use JSONB without abusing it
- [ ] I can choose B-tree, GIN, GiST, and BRIN indexes
- [ ] I can use partial and covering indexes
- [ ] I can use full-text search for moderate search needs
- [ ] I can use materialized views for expensive summaries
- [ ] I understand partitioning basics
- [ ] I can use row locks and `FOR UPDATE SKIP LOCKED`
- [ ] I can design outbox, audit log, and idempotency tables
- [ ] I understand autovacuum, analyze, connection pooling, and slow query monitoring

## MongoDB

- [ ] I can model documents around access patterns
- [ ] I can decide embed vs reference
- [ ] I can write find queries
- [ ] I can write aggregation pipelines
- [ ] I can design indexes
- [ ] I can use explain
- [ ] I can reason about shard keys

## Cassandra

- [ ] I can start from queries
- [ ] I can design partition keys
- [ ] I can design clustering columns
- [ ] I can keep partitions bounded
- [ ] I can denormalize intentionally
- [ ] I understand consistency levels
- [ ] I understand TTL/tombstone risks
- [ ] I know when Cassandra is the wrong choice

## Backend DB Judgment

- [ ] I can choose SQL vs MongoDB vs Cassandra
- [ ] I can separate OLTP from analytics
- [ ] I can use caches without making them source of truth accidentally
- [ ] I can design pagination safely
- [ ] I can prevent duplicate writes with constraints/idempotency
- [ ] I can design backup and restore strategy
- [ ] I can define database observability metrics

---

# North-Star Mental Model

Database mastery is not memorizing syntax.

It is asking:

```text
What question must this system answer,
how often,
for how much data,
under what correctness requirements,
and what structure makes that answer cheap and safe?
```

SQL gives you flexible correctness and powerful queries.

MongoDB gives you document-shaped modeling when aggregate reads dominate.

Cassandra gives you massive distributed query-specific tables when access patterns are known and writes are huge.

The senior skill is knowing which one not to use.
