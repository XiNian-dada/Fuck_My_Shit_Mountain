# Concurrency Audit Prompt

Use the fuck-my-shit-mountain skill in **concurrency mode**.

Shared setup, coverage, report template, HTML, and lint rules live in `references/report-format.md`; load that reference before producing the report.

Focus on race conditions, deadlocks, atomicity violations, shared state management, and synchronization correctness.

## Audit Areas (see principles 6.1–6.4, 10.3)

### Race Conditions
- Shared mutable state accessed without synchronization
- Time-of-check to time-of-use (TOCTOU) bugs
- Read-modify-write operations without atomics or locks
- Non-atomic operations on shared state (e.g., map updates, counter increments)
- Concurrent reads and writes to the same memory
- Visibility issues (memory ordering, cache coherence)
- Double-checked locking patterns without proper barriers

### Deadlocks & Livelocks
- Lock ordering violations (acquiring locks in inconsistent order)
- Circular wait conditions
- Nested lock acquisition without ordering discipline
- Lock held while waiting on a condition/channel/future
- Database transaction nesting or multi-connection deadlocks
- Distributed lock coordination issues
- Livelock scenarios (threads continuously yielding without progress)

### Atomicity & Consistency
- Missing transaction boundaries for multi-step operations
- Partial updates visible to concurrent readers
- Invariant violations during concurrent modification
- Lost updates (concurrent writes overwriting each other)
- ABA problems in lock-free data structures
- Torn reads/writes (non-atomic access to multi-word values)
- Inconsistent snapshot reads across multiple variables

### Synchronization Primitives
- Missing locks or barriers
- Locks that are too coarse (global locks causing contention)
- Locks that are too fine (missing composite atomicity)
- Read-write lock misuse (upgrading read lock to write lock)
- Condition variable usage without proper predicate checking
- Semaphore/channel misuse (capacity, signaling protocol)
- Atomic operations with incorrect memory ordering

### Thread/Task Safety
- Thread-unsafe library usage in concurrent context
- Global/static mutable state without protection
- Lazy initialization without double-checked locking or once-semantics
- Thread-local storage misuse
- Async task cancellation leaving inconsistent state
- Concurrent access to non-thread-safe collections (e.g., HashMap in Java without ConcurrentHashMap)

### Resource Contention
- Lock contention on hot paths (measured or inferred)
- False sharing (cache line bouncing)
- Lock-free alternatives that would reduce contention
- Reader-writer imbalance (many writers starving readers, or vice versa)
- Priority inversion scenarios
- Spin locks in high-latency contexts

### Producer-Consumer Patterns
- Unbounded queue growth without backpressure
- Queue/channel shutdown coordination issues
- Missing or incorrect use of close/done signals
- Multiple consumers without work-stealing or fair distribution
- Priority queue starvation
- Blocking operations inside critical sections

### Testing & Observability
- Missing race detection in test runs (e.g., `-race` in Go, ThreadSanitizer)
- Lack of stress tests for concurrent code paths
- Deadlock detection tooling not used
- Lock wait time not instrumented or alerted on
- No visibility into lock contention metrics

## Rules

1. Focus on realistic failure scenarios that can manifest under production load.
2. For each issue, describe the interleaving that causes failure, the observable symptom, and the user-visible impact.
3. Prefer the minimal fix that removes the race or deadlock risk — often adding proper synchronization or reordering locks.
4. Consider performance impact: over-synchronization can kill throughput, so recommend the right granularity.
5. When lock-free alternatives exist and are safe, mention them as a long-term fix.

## Attitude

3. **Test evidence matters.** Missing race detection or stress tests is a confidence gap. Report it as a finding only when a reachable concurrent path and a meaningful regression-verification gap are demonstrated.

## Finding Format

Use the common fields in `templates/issue-card.md` and the format rules in `references/report-format.md`. Specialized evidence supplements those fields; it does not replace them.

Include these additional details when they help substantiate a finding:

- Concurrent interleaving:
