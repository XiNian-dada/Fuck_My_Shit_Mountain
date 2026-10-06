# Data Integrity Audit Prompt

Use the fuck-my-shit-mountain skill in **data-integrity mode**.

Shared setup, coverage, report template, HTML, and lint rules live in `references/report-format.md`; load that reference before producing the report.

Focus on whether the system preserves correct, durable, and recoverable data under failures, retries, concurrency, and upgrades.

## Audit Areas

### Transaction Boundaries
- Multi-step writes without a transaction or equivalent atomicity guarantee.
- External I/O performed while holding a transaction open.
- Partial writes when a later operation fails.
- Transaction retries missing for serialization/conflict errors.
- Business invariants split across application code and database constraints.

### Idempotency and Retries
- POST/job/message handlers that are unsafe to retry.
- Duplicate submissions create duplicate records or side effects.
- Idempotency keys accepted but not enforced durably.
- Background jobs can run twice after crash/restart.
- Retry logic repeats non-idempotent external calls.

### Concurrency Consistency
- Lost update risks from read-modify-write without locking or compare-and-swap.
- Missing optimistic locking/version checks on mutable records.
- Race conditions between scheduled jobs and user actions.
- Queue consumers process the same item concurrently.
- Cache writes can overwrite newer data with stale data.

### Migrations and Schema Evolution
- Migrations cannot be run repeatedly or safely after partial failure.
- Schema and application changes require impossible deployment ordering.
- Missing backward/forward compatibility during rolling deploys.
- No rollback plan for destructive migrations.
- Data backfills lack progress tracking or restart safety.

### Validation and Invariants
- Invalid data can enter persistence because validation only happens in UI/client code.
- Database constraints are missing for core invariants.
- Derived values can drift from source-of-truth records.
- Soft deletes, status transitions, or lifecycle states allow impossible combinations.
- Timestamps, time zones, or ordering assumptions can corrupt business meaning.

### Backup, Restore, and Reconciliation
- Backup exists but restore is untested.
- No reconciliation job for eventually consistent data.
- No audit trail for high-impact mutations.
- Deletes or destructive updates cannot be recovered.
- Export/import paths lose precision, encoding, or identity.

## Rules

1. Every data-integrity finding must identify the invariant that can be violated.
2. Prefer local fixes: transaction, constraint, idempotency key, version check, or migration guard.
3. Treat data loss/corruption on normal operation as Critical.
4. Distinguish performance denormalization from unsafe duplication; denormalization is acceptable if reconciliation exists.
5. For each issue, include a regression test that simulates failure, retry, or concurrency when practical.


## Finding Format

Use the common fields in `templates/issue-card.md` and the format rules in `references/report-format.md`. Specialized evidence supplements those fields; it does not replace them.

Include these additional details when they help substantiate a finding:

- Subtype: TransactionBoundary / Idempotency / ConcurrencyConsistency / MigrationSafety / InvariantValidation / BackupRestore / Reconciliation
- Invariant at risk:
