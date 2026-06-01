# DSA Learning Roadmap for Backend Developers

A practical, deep, project-driven roadmap for learning Data Structures and Algorithms as a backend developer.

This roadmap avoids books and videos by design. It favors high-quality online reading, interactive references, problem sets, implementation practice, and progress checkpoints.

---

## Guiding Principle

Learn DSA from system behavior, not from abstract puzzles first.

As a backend developer, DSA is not just for interviews. It helps you understand performance, database indexes, queues, caches, schedulers, search, ranking, rate limiting, graph traversal, parsing, and distributed systems.

The right learning order is:

```text
concrete backend problem
-> data structure choice
-> algorithm behavior
-> complexity analysis
-> implementation
-> tradeoffs
```

Do not start by memorizing 300 patterns. Build intuition first, then pattern recognition.

---

## Roadmap Overview

Suggested duration: 12-18 weeks

Suggested weekly effort: 6-10 hours

Main outcome: you should be able to reason about performance, choose the right data structure, solve common algorithmic problems, and recognize DSA concepts inside backend systems.

| Level | Theme | Main Skill |
|---|---|---|
| 0 | Foundations | Understand complexity, memory, and problem-solving workflow |
| 1 | Arrays and Strings | Master sequential data and pointer-based thinking |
| 2 | Hashing | Build fast lookup, counting, grouping, and deduplication systems |
| 3 | Stacks and Queues | Model order, history, scheduling, and streaming behavior |
| 4 | Linked Lists | Understand pointer manipulation and structural mutation |
| 5 | Recursion and Backtracking | Explore decision trees and search spaces |
| 6 | Sorting and Binary Search | Control order, boundaries, and logarithmic search |
| 7 | Trees and Heaps | Model hierarchy, priority, ranking, and indexing |
| 8 | Graphs | Model relationships, dependencies, networks, and reachability |
| 9 | Dynamic Programming | Optimize repeated subproblems and state transitions |
| 10 | Tries, Intervals, and Advanced Patterns | Build autocomplete, calendars, ranges, and search systems |
| 11 | Backend-Oriented DSA | Apply DSA to caches, queues, indexes, rate limiters, and schedulers |

---

# Level 0: Foundations

## Goal

Build the mental tools for analyzing code and choosing better approaches.

## Core Concepts

| Concept | Backend-Friendly Meaning |
|---|---|
| Time complexity | How runtime grows as input grows |
| Space complexity | How memory usage grows as input grows |
| Big O | Upper-bound language for growth |
| Input size | Number of users, rows, requests, events, edges, files, tokens |
| Constant factors | Practical cost hidden by Big O |
| Tradeoff | Usually speed vs memory vs complexity |
| Invariant | A condition that stays true while an algorithm runs |
| Edge case | Input that breaks lazy assumptions |

## Learn

- Big O, Big Omega, and Big Theta at a practical level
- Common complexities: O(1), O(log n), O(n), O(n log n), O(n^2), O(2^n)
- Difference between worst-case, average-case, and amortized cost
- Why nested loops are not always O(n^2)
- Why two separate loops are usually O(n), not O(2n)
- How to estimate memory usage
- How to reason from constraints

## Reading Resources

- [Big-O Cheat Sheet](https://www.bigocheatsheet.com/)
- [CP-Algorithms](https://cp-algorithms.com/)
- [VisuAlgo](https://visualgo.net/en)
- [HackerRank Data Structures](https://www.hackerrank.com/domains/data-structures)
- [HackerRank Algorithms](https://www.hackerrank.com/domains/algorithms)

## Practice Method

For every problem, write this before coding:

```text
Input size:
Brute force idea:
Brute force complexity:
Better idea:
Data structure needed:
Invariant:
Edge cases:
```

## Completion Checkpoint

You can look at code and explain whether it is O(n), O(n log n), O(n^2), or worse.

## Tracker

- [ ] I understand Big O notation
- [ ] I can identify common runtime classes
- [ ] I can explain space complexity
- [ ] I understand amortized cost
- [ ] I can use constraints to reject slow solutions
- [ ] I can write a brute force solution before optimizing

---

# Level 1: Arrays and Strings

## Goal

Master sequential data, indexes, windows, and pointer movement.

Arrays and strings are the ground floor of DSA. Most backend data eventually becomes a sequence: logs, requests, rows, events, characters, tokens, timestamps.

## Learn

| Pattern | What It Solves |
|---|---|
| Linear scan | Find, count, validate |
| Two pointers | Compare ends, merge, partition |
| Sliding window | Contiguous subarray or substring problems |
| Prefix sum | Fast range queries |
| Difference array | Fast range updates |
| In-place mutation | Reduce extra memory |
| Character counting | String frequency and validation |

## Backend Connections

| DSA Idea | Backend Example |
|---|---|
| Sliding window | Rate limiting, rolling metrics, recent activity |
| Prefix sums | Analytics over time ranges |
| Two pointers | Merging sorted logs or event streams |
| String parsing | Request validation, log processing, tokenization |

## Project: Log Window Analyzer

Build a small utility that processes timestamped request logs.

Input:

```text
user_id, timestamp, endpoint, status_code
```

Features:

```text
- count requests per user
- find users exceeding N requests in a rolling 60-second window
- calculate error rate over time ranges
- merge logs from two sorted files
```

## Reading Resources

- [GeeksforGeeks: Two Pointers Technique](https://www.geeksforgeeks.org/two-pointers-technique/)
- [GeeksforGeeks: Sliding Window Technique](https://www.geeksforgeeks.org/window-sliding-technique/)
- [Python Sequence Types](https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range)
- [HackerRank Arrays Practice](https://www.hackerrank.com/domains/data-structures/arrays)

## Must-Solve Problems

- Two Sum
- Best Time to Buy and Sell Stock
- Valid Palindrome
- Merge Sorted Array
- Maximum Subarray
- Product of Array Except Self
- Longest Substring Without Repeating Characters
- Minimum Size Subarray Sum
- Subarray Sum Equals K

## Completion Checkpoint

You can see a contiguous range problem and know whether to try sliding window, prefix sum, or brute force.

## Tracker

- [ ] I can scan arrays and strings confidently
- [ ] I understand two pointers
- [ ] I understand sliding windows
- [ ] I understand prefix sums
- [ ] I can merge sorted sequences
- [ ] I completed the Log Window Analyzer

---

# Level 2: Hashing

## Goal

Use hash maps and hash sets for fast lookup, counting, grouping, and deduplication.

Hashing is probably the most backend-relevant DSA topic. It shows up in caches, indexes, deduplication, joins, session storage, idempotency keys, routing, and frequency counters.

## Learn

| Pattern | What It Solves |
|---|---|
| Hash set lookup | Fast existence checks |
| Hash map counting | Frequency and aggregation |
| Grouping | Bucketing records by key |
| Reverse index | Find items by derived property |
| Seen-state tracking | Cycle detection and deduplication |
| Composite keys | Multi-field lookup |
| Hash collisions | Why worst-case can degrade |

## Backend Connections

| DSA Idea | Backend Example |
|---|---|
| Hash map | In-memory cache |
| Hash set | Idempotency key tracking |
| Group by key | Analytics aggregation |
| Consistent hashing | Distributed cache routing |
| Composite key | Multi-tenant lookup |

## Project: Idempotency and Deduplication Service

Build a small service that accepts events and prevents duplicates.

Input:

```json
{
  "idempotency_key": "abc-123",
  "user_id": "u1",
  "event_type": "payment.created",
  "payload": {}
}
```

Features:

```text
- reject duplicate idempotency keys
- count events by type
- group events by user
- expire old keys after TTL
```

## Reading Resources

- [Python Dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)
- [Java HashMap](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashMap.html)
- [Wikipedia: Hash Table](https://en.wikipedia.org/wiki/Hash_table)
- [GeeksforGeeks: Hashing Data Structure](https://www.geeksforgeeks.org/hashing-data-structure/)

## Must-Solve Problems

- Contains Duplicate
- Valid Anagram
- Group Anagrams
- Top K Frequent Elements
- Longest Consecutive Sequence
- First Unique Character in a String
- Isomorphic Strings
- Subarray Sum Equals K

## Completion Checkpoint

You can identify when a nested loop can be replaced by a hash map or hash set.

## Tracker

- [ ] I understand hash maps
- [ ] I understand hash sets
- [ ] I can count frequencies
- [ ] I can group by key
- [ ] I can use composite keys
- [ ] I understand collisions at a high level
- [ ] I completed the Idempotency and Deduplication Service

---

# Level 3: Stacks and Queues

## Goal

Understand order-sensitive systems: history, undo, scheduling, breadth-first traversal, and streaming.

Stacks and queues are small but powerful. They teach you how execution order changes behavior.

## Learn

| Structure | Behavior | Backend Example |
|---|---|---|
| Stack | Last in, first out | Call stack, undo, parsing |
| Queue | First in, first out | Job queues, request queues |
| Deque | Add/remove both ends | Sliding windows, schedulers |
| Monotonic stack | Keep ordered candidates | Next greater item, spans |
| Monotonic queue | Window min/max | Rolling metrics |
| Priority queue | Highest priority first | Job scheduling |

## Project: Job Queue Simulator

Build a job queue simulator.

Features:

```text
- enqueue jobs
- process FIFO jobs
- retry failed jobs
- support priority jobs
- track queue wait time
- simulate worker concurrency
```

## Reading Resources

- [Python collections.deque](https://docs.python.org/3/library/collections.html#collections.deque)
- [Python heapq](https://docs.python.org/3/library/heapq.html)
- [GeeksforGeeks: Stack Data Structure](https://www.geeksforgeeks.org/stack-data-structure/)
- [GeeksforGeeks: Queue Data Structure](https://www.geeksforgeeks.org/queue-data-structure/)
- [VisuAlgo: Stack and Queue](https://visualgo.net/en/list)

## Must-Solve Problems

- Valid Parentheses
- Min Stack
- Implement Queue using Stacks
- Daily Temperatures
- Next Greater Element
- Sliding Window Maximum
- Evaluate Reverse Polish Notation
- Number of Recent Calls

## Completion Checkpoint

You can explain why BFS uses a queue and DFS often uses a stack or recursion.

## Tracker

- [ ] I understand stacks
- [ ] I understand queues
- [ ] I understand deques
- [ ] I can use a heap as a priority queue
- [ ] I understand monotonic stacks
- [ ] I completed the Job Queue Simulator

---

# Level 4: Linked Lists

## Goal

Understand pointer manipulation, mutation, and references.

Linked lists are less common in everyday backend code, but they are useful for understanding memory references, caches, queues, and interview-style pointer reasoning.

## Learn

| Topic | What To Learn |
|---|---|
| Node references | Value plus pointer to next node |
| Traversal | Moving through a chain |
| Insertion/deletion | Updating pointers safely |
| Dummy nodes | Simplify edge cases |
| Fast/slow pointers | Detect cycles and find middle |
| Reversal | Change direction of links |
| Doubly linked list | Previous and next references |

## Backend Connections

| DSA Idea | Backend Example |
|---|---|
| Doubly linked list | LRU cache order tracking |
| Fast/slow pointer | Cycle detection |
| Pointer updates | Mutable object graph reasoning |
| Dummy node | Cleaner edge-case handling |

## Project: LRU Cache from Scratch

Build an LRU cache using:

```text
hash map + doubly linked list
```

Features:

```text
- get(key)
- put(key, value)
- evict least recently used item
- O(1) get
- O(1) put
```

## Reading Resources

- [GeeksforGeeks: Linked List Data Structure](https://www.geeksforgeeks.org/data-structures/linked-list/)
- [Wikipedia: Linked List](https://en.wikipedia.org/wiki/Linked_list)
- [HackerRank Linked Lists Practice](https://www.hackerrank.com/domains/data-structures/linked-lists)

## Must-Solve Problems

- Reverse Linked List
- Merge Two Sorted Lists
- Linked List Cycle
- Middle of the Linked List
- Remove Nth Node From End of List
- Reorder List
- Add Two Numbers
- LRU Cache

## Completion Checkpoint

You can reverse a linked list and explain every pointer change without hand-waving.

## Tracker

- [ ] I understand node references
- [ ] I can traverse a linked list
- [ ] I can insert and delete nodes
- [ ] I understand dummy nodes
- [ ] I can detect cycles
- [ ] I can reverse a linked list
- [ ] I completed the LRU Cache from Scratch

---

# Level 5: Recursion and Backtracking

## Goal

Learn to explore decision trees systematically.

Recursion is not magic. It is a function calling itself with a smaller problem. Backtracking is recursion plus undoing choices.

## Mental Model

```text
choose
-> explore
-> undo choice
```

## Learn

| Topic | What To Learn |
|---|---|
| Base case | When recursion stops |
| Recursive case | How the problem gets smaller |
| Call stack | What is waiting to resume |
| Backtracking | Explore choices and undo state |
| Pruning | Avoid useless branches |
| Recursion tree | Visualize exponential behavior |

## Backend Connections

| DSA Idea | Backend Example |
|---|---|
| Recursion | Tree traversal, nested comments, org charts |
| Backtracking | Constraint solving, permissions, route planning |
| Pruning | Search optimization |
| Call stack limits | Production safety concern |

## Project: Permission Resolver

Build a recursive permission resolver.

Input:

```text
user -> roles -> groups -> inherited permissions
```

Features:

```text
- resolve final permissions
- handle nested groups
- detect cycles
- explain permission source path
```

## Reading Resources

- [GeeksforGeeks: Recursion](https://www.geeksforgeeks.org/recursion/)
- [GeeksforGeeks: Backtracking Algorithms](https://www.geeksforgeeks.org/backtracking-algorithms/)
- [Python Recursion Limit](https://docs.python.org/3/library/sys.html#sys.setrecursionlimit)

## Must-Solve Problems

- Subsets
- Permutations
- Combination Sum
- Letter Combinations of a Phone Number
- Generate Parentheses
- Word Search
- N-Queens
- Palindrome Partitioning

## Completion Checkpoint

You can draw the recursion tree for subsets, permutations, and combination sum.

## Tracker

- [ ] I understand base cases
- [ ] I understand recursive cases
- [ ] I understand the call stack
- [ ] I can write backtracking code
- [ ] I can prune invalid branches
- [ ] I completed the Permission Resolver

---

# Level 6: Sorting and Binary Search

## Goal

Master order.

Sorting and binary search are foundational because many optimizations begin by introducing order.

## Learn

| Topic | What To Learn |
|---|---|
| Sorting basics | Why sorting often costs O(n log n) |
| Stable sort | Preserve relative order of equal elements |
| Custom comparator | Sort by derived business logic |
| Binary search | Search in sorted space |
| Boundary search | First true, last false, lower bound |
| Search on answer | Binary search over possible result values |
| Merge intervals | Sorting plus range merging |

## Backend Connections

| DSA Idea | Backend Example |
|---|---|
| Sorting | Ranking, pagination, leaderboards |
| Binary search | Index lookup, time-series search |
| Stable sort | Multi-level ordering |
| Search on answer | Capacity planning, throttling thresholds |
| Interval merging | Calendars, bookings, rate windows |

## Project: Time Range Query Engine

Build a utility for time ranges.

Features:

```text
- store sorted events
- find events between start and end timestamps
- merge overlapping maintenance windows
- detect booking conflicts
- find first event after timestamp
```

## Reading Resources

- [CP-Algorithms: Binary Search](https://cp-algorithms.com/num_methods/binary_search.html)
- [Python bisect](https://docs.python.org/3/library/bisect.html)
- [Python Sorting HOWTO](https://docs.python.org/3/howto/sorting.html)
- [VisuAlgo: Sorting](https://visualgo.net/en/sorting)

## Must-Solve Problems

- Binary Search
- Search Insert Position
- First Bad Version
- Search in Rotated Sorted Array
- Find Minimum in Rotated Sorted Array
- Koko Eating Bananas
- Merge Intervals
- Insert Interval
- Meeting Rooms
- Meeting Rooms II

## Completion Checkpoint

You can write binary search without guessing indexes forever. You know what invariant your loop preserves.

## Tracker

- [ ] I understand O(n log n) sorting
- [ ] I can use custom sort keys
- [ ] I can write binary search
- [ ] I understand lower bound and upper bound
- [ ] I can merge intervals
- [ ] I completed the Time Range Query Engine

---

# Level 7: Trees and Heaps

## Goal

Understand hierarchical data, priority, and indexing.

Trees are everywhere: file systems, org charts, comments, JSON, DOM, syntax trees, database indexes, and decision trees.

## Learn

| Topic | What To Learn |
|---|---|
| Binary tree | Node with left and right children |
| DFS traversal | Preorder, inorder, postorder |
| BFS traversal | Level-order traversal |
| Binary search tree | Left smaller, right larger |
| Balanced trees | Keep operations logarithmic |
| Heap | Efficient min/max priority access |
| Top K | Find highest/lowest K items efficiently |

## Backend Connections

| DSA Idea | Backend Example |
|---|---|
| Tree traversal | Nested comments, folders, org hierarchy |
| BST | Ordered lookup concept behind indexes |
| B-tree/B+tree | Database indexes |
| Heap | Priority jobs, top K queries |
| Trie | Prefix search and autocomplete |

## Project: Hierarchical Comment System

Build nested comments.

Features:

```text
- add comment
- reply to comment
- return nested tree
- return flattened thread order
- calculate max depth
- hide deleted branches safely
```

Optional extension:

```text
Build a priority job scheduler with a heap.
```

## Reading Resources

- [GeeksforGeeks: Tree Data Structure](https://www.geeksforgeeks.org/introduction-to-tree-data-structure/)
- [GeeksforGeeks: Binary Tree Data Structure](https://www.geeksforgeeks.org/binary-tree-data-structure/)
- [Python heapq](https://docs.python.org/3/library/heapq.html)
- [VisuAlgo: Binary Heap](https://visualgo.net/en/heap)
- [Use The Index, Luke: Anatomy of an Index](https://use-the-index-luke.com/sql/anatomy)

## Must-Solve Problems

- Maximum Depth of Binary Tree
- Invert Binary Tree
- Same Tree
- Binary Tree Level Order Traversal
- Validate Binary Search Tree
- Kth Smallest Element in a BST
- Lowest Common Ancestor of a BST
- Top K Frequent Elements
- Kth Largest Element in an Array
- Find Median from Data Stream

## Completion Checkpoint

You can traverse a tree with DFS and BFS, and you can explain when a heap is better than sorting.

## Tracker

- [ ] I understand binary trees
- [ ] I can write DFS traversals
- [ ] I can write BFS traversals
- [ ] I understand binary search trees
- [ ] I understand heaps
- [ ] I can solve Top K problems
- [ ] I completed the Hierarchical Comment System

---

# Level 8: Graphs

## Goal

Model relationships, dependencies, networks, and reachability.

Graphs are one of the most important backend DSA topics. They show up in dependency resolution, recommendation systems, social graphs, permissions, workflows, routing, fraud rings, service dependency maps, and build systems.

## Learn

| Topic | What To Learn |
|---|---|
| Graph representation | Adjacency list, adjacency matrix, edge list |
| Directed vs undirected | One-way vs two-way relationships |
| Weighted graph | Edges have costs |
| BFS | Shortest path in unweighted graphs |
| DFS | Reachability, components, cycle detection |
| Topological sort | Dependency ordering |
| Union-Find | Connectivity and grouping |
| Dijkstra | Shortest path with non-negative weights |
| Minimum spanning tree | Connect all nodes cheaply |

## Backend Connections

| DSA Idea | Backend Example |
|---|---|
| BFS | Shortest friend path, nearest service node |
| DFS | Permission inheritance, dependency traversal |
| Topological sort | Job dependencies, build pipelines, migrations |
| Union-Find | Group accounts, merge identities |
| Dijkstra | Routing, network cost, delivery optimization |
| Cycle detection | Prevent recursive dependency loops |

## Project: Dependency Resolver

Build a dependency resolver for jobs or services.

Input:

```json
{
  "jobs": ["extract", "transform", "load", "notify"],
  "dependencies": [
    ["transform", "extract"],
    ["load", "transform"],
    ["notify", "load"]
  ]
}
```

Features:

```text
- return valid execution order
- detect cycles
- list blocked jobs
- support parallel execution batches
```

## Reading Resources

- [CP-Algorithms: Graph Algorithms](https://cp-algorithms.com/graph/)
- [GeeksforGeeks: Graph Data Structure and Algorithms](https://www.geeksforgeeks.org/graph-data-structure-and-algorithms/)
- [VisuAlgo: Graph Traversal](https://visualgo.net/en/dfsbfs)
- [VisuAlgo: Minimum Spanning Tree](https://visualgo.net/en/mst)
- [VisuAlgo: Shortest Paths](https://visualgo.net/en/sssp)

## Must-Solve Problems

- Number of Islands
- Clone Graph
- Course Schedule
- Course Schedule II
- Pacific Atlantic Water Flow
- Rotting Oranges
- Network Delay Time
- Redundant Connection
- Accounts Merge
- Word Ladder

## Completion Checkpoint

You can choose between BFS, DFS, topological sort, Union-Find, and Dijkstra based on the problem statement.

## Tracker

- [ ] I can represent graphs
- [ ] I can write BFS
- [ ] I can write DFS
- [ ] I can detect cycles
- [ ] I understand topological sort
- [ ] I understand Union-Find
- [ ] I understand Dijkstra at a practical level
- [ ] I completed the Dependency Resolver

---

# Level 9: Dynamic Programming

## Goal

Learn to optimize repeated subproblems.

Dynamic programming is where many people suffer because they start with formulas. Start instead with recursion, repeated work, and state.

## Mental Model

```text
brute force recursion
-> identify repeated subproblems
-> define state
-> cache results
-> optionally convert to bottom-up table
```

## Learn

| Topic | What To Learn |
|---|---|
| Overlapping subproblems | Same work appears many times |
| Optimal substructure | Best answer built from smaller best answers |
| Memoization | Top-down recursion plus cache |
| Tabulation | Bottom-up table filling |
| State definition | What variables uniquely identify subproblem? |
| Transition | How one state moves to another |
| 1D DP | Linear state |
| 2D DP | Two-dimensional state |
| Knapsack | Choose/skip decision pattern |
| Sequence DP | Strings, subsequences, edit distance |

## Backend Connections

| DSA Idea | Backend Example |
|---|---|
| Memoization | Cache repeated computations |
| State transition | Workflow engines |
| Knapsack | Resource allocation |
| Edit distance | Fuzzy matching, search correction |
| Sequence DP | Diff tools, text similarity |

## Project: Pricing and Discount Optimizer

Build a discount optimizer.

Input:

```text
cart items, discount rules, budget constraints
```

Features:

```text
- maximize discount under constraints
- avoid invalid combinations
- explain selected discounts
- compare brute force vs memoized solution
```

## Reading Resources

- [CP-Algorithms: Dynamic Programming Introduction](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html)
- [GeeksforGeeks: Dynamic Programming](https://www.geeksforgeeks.org/dynamic-programming/)
- [CSES Dynamic Programming Problem Set](https://cses.fi/problemset/list/)
- [USACO Guide: Dynamic Programming](https://usaco.guide/gold/dp)

## Must-Solve Problems

- Climbing Stairs
- House Robber
- Coin Change
- Longest Increasing Subsequence
- Longest Common Subsequence
- Word Break
- Combination Sum IV
- Unique Paths
- Partition Equal Subset Sum
- Edit Distance

## Completion Checkpoint

For a DP problem, you can write:

```text
State:
Transition:
Base case:
Answer:
Complexity:
```

## Tracker

- [ ] I understand memoization
- [ ] I understand tabulation
- [ ] I can define DP state
- [ ] I can write transitions
- [ ] I can solve basic 1D DP
- [ ] I can solve basic 2D DP
- [ ] I completed the Pricing and Discount Optimizer

---

# Level 10: Tries, Intervals, and Advanced Patterns

## Goal

Learn specialized structures and patterns that appear often in backend systems.

## Learn

| Topic | Backend Use |
|---|---|
| Trie | Autocomplete, prefix search, routing |
| Interval merging | Calendars, bookings, maintenance windows |
| Sweep line | Concurrent events, active sessions |
| Fenwick tree | Fast prefix sums with updates |
| Segment tree | Range queries and range updates |
| Bloom filter | Probabilistic membership checks |
| LRU/LFU | Cache eviction policies |
| Consistent hashing | Distributed cache/database sharding |

## Project: Autocomplete and Calendar Engine

Part 1: autocomplete.

Features:

```text
- insert search terms
- prefix lookup
- rank suggestions by frequency
```

Part 2: calendar engine.

Features:

```text
- add events
- merge overlapping intervals
- detect conflicts
- find free slots
```

## Reading Resources

- [GeeksforGeeks: Trie Data Structure](https://www.geeksforgeeks.org/trie-insert-and-search/)
- [CP-Algorithms: Fenwick Tree](https://cp-algorithms.com/data_structures/fenwick.html)
- [CP-Algorithms: Segment Tree](https://cp-algorithms.com/data_structures/segment_tree.html)
- [Wikipedia: Bloom Filter](https://en.wikipedia.org/wiki/Bloom_filter)
- [Wikipedia: Consistent Hashing](https://en.wikipedia.org/wiki/Consistent_hashing)

## Must-Solve Problems

- Implement Trie
- Design Add and Search Words Data Structure
- Word Search II
- Merge Intervals
- Insert Interval
- Non-overlapping Intervals
- Meeting Rooms II
- My Calendar I
- LRU Cache
- LFU Cache

## Completion Checkpoint

You can identify when a specialized structure is worth the implementation complexity.

## Tracker

- [ ] I understand tries
- [ ] I understand interval merging
- [ ] I understand sweep line basics
- [ ] I understand Fenwick trees at a practical level
- [ ] I understand segment trees at a practical level
- [ ] I understand Bloom filters conceptually
- [ ] I understand consistent hashing conceptually
- [ ] I completed the Autocomplete and Calendar Engine

---

# Level 11: Backend-Oriented DSA

## Goal

Connect DSA to real backend architecture.

This is where DSA stops feeling like interview trivia and starts becoming engineering leverage.

## Systems To Understand

| System | DSA Inside |
|---|---|
| LRU cache | Hash map + doubly linked list |
| Priority queue worker | Heap |
| Rate limiter | Sliding window, token bucket, leaky bucket |
| Database index | B-tree/B+tree |
| Full-text search | Inverted index, trie, ranking |
| Autocomplete | Trie + heap/top K |
| Job scheduler | Heap + graph dependencies |
| Workflow engine | State machine + graph |
| API gateway routing | Trie or radix tree |
| Deduplication | Hash set + TTL |
| Metrics aggregation | Hash maps, prefix sums, sketches |
| Distributed cache | Consistent hashing |
| Fraud detection | Graph traversal |

## Project: Backend DSA Mini-System Suite

Build these small components from scratch:

```text
- LRU cache
- sliding-window rate limiter
- priority job queue
- dependency scheduler
- autocomplete service
- interval booking service
```

Then write one short design note for each:

```text
Data structure used:
Why this structure:
Time complexity:
Space complexity:
Production limitations:
```

## Reading Resources

- [Use The Index, Luke](https://use-the-index-luke.com/)
- [Redis Data Types](https://redis.io/docs/latest/develop/data-types/)
- [Cloudflare: Counting Things a Lot of Different Things](https://blog.cloudflare.com/counting-things-a-lot-of-different-things/)
- [System Design Primer: Algorithms](https://github.com/donnemartin/system-design-primer#algorithms)

## Completion Checkpoint

You can look at a backend feature and describe the data structures that make it efficient.

## Tracker

- [ ] I can implement an LRU cache
- [ ] I can implement a rate limiter
- [ ] I can implement a priority queue scheduler
- [ ] I can implement dependency ordering
- [ ] I can implement autocomplete
- [ ] I can implement interval conflict detection
- [ ] I can explain the tradeoffs of each design

---

# 16-Week Progress Plan

## Weeks 1-2: Complexity, Arrays, and Strings

- [ ] Learn Big O and space complexity
- [ ] Practice linear scans and two pointers
- [ ] Practice sliding window
- [ ] Practice prefix sums
- [ ] Build Log Window Analyzer

## Weeks 3-4: Hashing, Stacks, and Queues

- [ ] Learn hash maps and hash sets
- [ ] Practice grouping and counting
- [ ] Learn stacks and queues
- [ ] Learn heaps as priority queues
- [ ] Build Idempotency and Deduplication Service
- [ ] Build Job Queue Simulator

## Weeks 5-6: Linked Lists, Recursion, and Backtracking

- [ ] Learn linked list pointer operations
- [ ] Build LRU Cache from Scratch
- [ ] Learn recursion and call stack
- [ ] Learn backtracking
- [ ] Build Permission Resolver

## Weeks 7-8: Sorting, Binary Search, Trees, and Heaps

- [ ] Learn sorting tradeoffs
- [ ] Learn binary search invariants
- [ ] Practice interval problems
- [ ] Learn tree traversal
- [ ] Learn heap-based Top K problems
- [ ] Build Time Range Query Engine
- [ ] Build Hierarchical Comment System

## Weeks 9-10: Graphs

- [ ] Learn graph representations
- [ ] Practice BFS and DFS
- [ ] Learn cycle detection
- [ ] Learn topological sort
- [ ] Learn Union-Find
- [ ] Learn Dijkstra
- [ ] Build Dependency Resolver

## Weeks 11-12: Dynamic Programming

- [ ] Learn memoization
- [ ] Learn tabulation
- [ ] Practice 1D DP
- [ ] Practice 2D DP
- [ ] Practice knapsack-style choices
- [ ] Practice sequence DP
- [ ] Build Pricing and Discount Optimizer

## Weeks 13-14: Advanced Structures

- [ ] Learn tries
- [ ] Learn interval and sweep-line patterns
- [ ] Learn Fenwick tree basics
- [ ] Learn segment tree basics
- [ ] Learn Bloom filters conceptually
- [ ] Learn consistent hashing conceptually
- [ ] Build Autocomplete and Calendar Engine

## Weeks 15-16: Backend DSA Capstone

Build the Backend DSA Mini-System Suite:

- [ ] LRU cache
- [ ] Sliding-window rate limiter
- [ ] Priority job queue
- [ ] Dependency scheduler
- [ ] Autocomplete service
- [ ] Interval booking service
- [ ] Design notes for each component

---

# Practice Strategy

## The 4-Pass Method

For each new pattern, solve problems in four passes.

Pass 1: Read and understand the pattern.

Pass 2: Solve 3-5 easy problems slowly.

Pass 3: Solve 5-8 medium problems without looking at solutions first.

Pass 4: Re-solve the same problems one week later from memory.

## How To Review a Problem

After each problem, write:

```text
Pattern:
Key insight:
Data structure:
Invariant:
Time complexity:
Space complexity:
Bug I almost made:
```

## When You Get Stuck

Do not stare forever.

Use this sequence:

```text
10 minutes: brute force
10 minutes: identify repeated work or expensive lookup
10 minutes: choose data structure
10 minutes: inspect one hint
then implement from your own understanding
```

---

# Problem Count Targets

Quality matters more than raw count, but useful targets are:

| Topic | Target Problems |
|---|---|
| Arrays and Strings | 25-35 |
| Hashing | 15-25 |
| Stacks and Queues | 15-20 |
| Linked Lists | 10-15 |
| Recursion and Backtracking | 15-20 |
| Sorting and Binary Search | 20-30 |
| Trees and Heaps | 25-35 |
| Graphs | 25-35 |
| Dynamic Programming | 25-40 |
| Advanced Patterns | 15-25 |

Total target: around 190-280 problems.

For backend competence, you do not need 500 random problems. You need deep pattern recognition plus real implementation projects.

---

# Best Problem Lists

Use these as your main sources. These are free to read and practice from.

- [CP-Algorithms](https://cp-algorithms.com/)
- [VisuAlgo](https://visualgo.net/en)
- [HackerRank Data Structures](https://www.hackerrank.com/domains/data-structures)
- [HackerRank Algorithms](https://www.hackerrank.com/domains/algorithms)
- [CSES Problem Set](https://cses.fi/problemset/)
- [USACO Guide](https://usaco.guide/)
- [GeeksforGeeks DSA](https://www.geeksforgeeks.org/learn-data-structures-and-algorithms-dsa-tutorial/)

Suggested order:

```text
VisuAlgo when a structure feels invisible
-> GeeksforGeeks for beginner-friendly explanations
-> HackerRank for basic-to-medium practice
-> CSES for clean problem sets and algorithmic stamina
-> CP-Algorithms for deeper explanations
-> USACO Guide for structured advanced practice
```

---

# What To Avoid

| Avoid | Reason |
|---|---|
| Memorizing solutions | Breaks under small variations |
| Only doing easy problems | Does not build pattern transfer |
| Only doing hard problems | Creates frustration without foundation |
| Skipping brute force | You lose the path to optimization |
| Ignoring complexity | You miss the reason the solution works |
| Jumping to DP too early | DP needs recursion and state intuition first |
| Solving random problems | Slower than topic-based progression |
| Using libraries too early | You miss the structure underneath |

---

# Interview-Oriented Pattern Map

| Problem Signal | Likely Pattern |
|---|---|
| Pair with target | Hash map or two pointers |
| Contiguous subarray | Sliding window or prefix sum |
| Sorted input | Binary search or two pointers |
| Top K | Heap or bucket sort |
| Nested hierarchy | Tree DFS/BFS |
| Dependencies | Topological sort |
| Shortest path unweighted | BFS |
| Shortest path weighted | Dijkstra |
| Connectivity | DFS/BFS or Union-Find |
| All combinations | Backtracking |
| Repeated subproblems | Dynamic programming |
| Prefix lookup | Trie |
| Overlapping ranges | Intervals or sweep line |
| Recent usage | LRU cache |
| Rolling request count | Sliding window rate limiter |

---

# Final Master Checklist

## Foundations

- [ ] I can analyze time complexity
- [ ] I can analyze space complexity
- [ ] I can use constraints to choose an algorithm
- [ ] I can explain brute force before optimizing
- [ ] I can describe invariants

## Core Data Structures

- [ ] I can use arrays and strings effectively
- [ ] I can use hash maps and hash sets
- [ ] I can use stacks and queues
- [ ] I can implement linked list operations
- [ ] I can use heaps and priority queues
- [ ] I can traverse trees
- [ ] I can represent graphs

## Core Algorithms

- [ ] I can use two pointers
- [ ] I can use sliding windows
- [ ] I can use prefix sums
- [ ] I can write binary search
- [ ] I can sort with custom keys
- [ ] I can write DFS
- [ ] I can write BFS
- [ ] I can write topological sort
- [ ] I can use Union-Find
- [ ] I can use Dijkstra when appropriate

## Advanced Patterns

- [ ] I can write backtracking solutions
- [ ] I can solve basic dynamic programming problems
- [ ] I can use tries for prefix search
- [ ] I can solve interval problems
- [ ] I understand Bloom filters conceptually
- [ ] I understand consistent hashing conceptually

## Backend Applications

- [ ] I can implement an LRU cache
- [ ] I can implement a rate limiter
- [ ] I can implement a priority job queue
- [ ] I can implement dependency scheduling
- [ ] I can implement autocomplete
- [ ] I can implement interval conflict detection
- [ ] I can explain DSA tradeoffs in backend systems

---

# North-Star Mental Model

DSA is not about clever puzzles.

DSA is about this question:

```text
Given the shape of the data and the operations we need,
what structure makes the important operation cheap?
```

For backend developers, this is the bridge between code that works and systems that scale.
