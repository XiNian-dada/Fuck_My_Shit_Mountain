# Observability Audit Prompt

Use the fuck-my-shit-mountain skill in **observability mode**.

Shared setup, coverage, report template, HTML, and lint rules live in `references/report-format.md`; load that reference before producing the report.

Focus on whether operators can understand, debug, and recover the system under realistic production failures.

## Audit Areas

### Logging
- Missing logs on critical state transitions, failures, and security-sensitive operations.
- Unstructured logs where structured fields are needed for search and correlation.
- Logs that lack request ID, trace ID, user/account ID, job ID, or operation name.
- Error logs that lose cause, stack, or relevant context.
- Sensitive data logged in clear text.

### Metrics
- No metrics for request volume, latency, error rate, saturation, queue depth, or worker lag.
- Counters used where histograms/gauges are needed, or vice versa.
- High-cardinality labels that can overload the metrics backend.
- Business-critical events with no measurable success/failure signal.
- No SLO-oriented metrics for user-visible workflows.

### Tracing and Correlation
- Request or job lifecycle cannot be followed across process/module boundaries.
- Background tasks lose correlation context.
- External calls lack span/operation labels.
- No correlation ID in client-facing errors or server logs.
- Distributed traces include too much irrelevant data and hide the failure path.

### Health and Readiness
- Health checks only prove the process is alive, not that dependencies are usable.
- Readiness checks do not reflect database/cache/message broker availability.
- Liveness checks can restart a process during long but healthy work.
- Startup probes do not account for migrations, warmup, or dependency initialization.
- No degradation signal when optional dependencies are unavailable.

### Alerting and Runbooks
- No alertable signal for critical failure modes.
- Alerts fire on symptoms with no actionable context.
- Missing runbook links or remediation steps for production alerts.
- Alert thresholds are static guesses and not tied to user impact.
- No escalation path for data loss, security, or availability incidents.

### Debuggability
- Error responses lack a safe correlation handle for support.
- CLI/admin tooling cannot inspect queues, stuck jobs, or state transitions.
- Feature flags or config changes cannot be audited.
- No way to reproduce or replay failed background work.
- Diagnostic endpoints expose sensitive data or lack authorization.

## Rules

1. Observability findings must describe the failure that would be hard to detect or debug.
2. Do not require enterprise telemetry for small projects; scale recommendations to the deployment model.
3. Prefer low-overhead instrumentation at boundaries: requests, jobs, external calls, persistence, and critical state transitions.
4. Treat logging sensitive data as a security finding as well as an observability problem.
5. For each issue, include the signal that should exist and where it should be emitted.


## Finding Format

Use the common fields in `templates/issue-card.md` and the format rules in `references/report-format.md`. Specialized evidence supplements those fields; it does not replace them.

Include these additional details when they help substantiate a finding:

- Subtype: Logging / Metrics / Tracing / HealthCheck / Alerting / Runbook / Debuggability
- Missing or unsafe signal:
- Why this matters:
