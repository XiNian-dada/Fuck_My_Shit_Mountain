# Performance Audit Prompt

Use the fuck-my-shit-mountain skill in **performance mode**.

Shared setup, coverage, report template, HTML, and lint rules live in `references/report-format.md`; load that reference before producing the report.

Focus on realistic bottlenecks, not premature micro-optimization.

## Audit Areas (see principle 10.2: Unbounded Resources)

### Hot Paths
- Request handler latency
- Inner loop performance
- Allocation frequency on hot paths
- Serialization/deserialization on critical paths

### Data Access
- Database query patterns (N+1, missing indexes, full table scans)
- Cache miss ratio
- Connection pool utilization
- Query result size
- Data pagination

### Concurrency & Locking
- Lock contention on hot paths
- Serialization bottlenecks
- Channel / queue backpressure
- Mutex / RwLock granularity

### Memory
- Unbounded collection growth
- Memory allocation patterns
- Object pooling or lack thereof
- Large object retention
- Memory fragmentation (GC languages)
- Slice / array copying on hot paths

### I/O
- Synchronous I/O in async context
- File I/O pattern (read size, buffering)
- Network round-trip count
- Payload size optimization
- Compression usage

### Frontend (if applicable)
- Re-render frequency
- Virtual DOM diff cost
- Bundle size
- Image / asset optimization
- Lazy loading
- List virtualization

### Startup & Initialization
- Cold start time
- Dependency loading
- Configuration parsing
- Lazy initialization opportunities

## Rules

1. Do not suggest optimization unless there is a realistic scale or workload where it matters.
2. Identify the bottleneck mechanism, not just the symptom.
3. Include the workload or conditions under which the issue becomes relevant.
4. Prefer small, targeted optimizations over architectural changes when sufficient.

## Attitude

1. **Be exhaustive.** Scan every hot path, every query, every allocation pattern. One unoptimized query can kill production at scale.


## Finding Format

Use the common fields in `templates/issue-card.md` and the format rules in `references/report-format.md`. Specialized evidence supplements those fields; it does not replace them.

Include these additional details when they help substantiate a finding:

- Workload where this matters:
- Bottleneck mechanism:
- Expected impact:
- Minimal optimization:
- Better long-term optimization:
- Benchmark or test suggestion:
