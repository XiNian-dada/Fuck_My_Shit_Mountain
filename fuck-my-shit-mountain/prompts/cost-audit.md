# Cost and Resource Economics Audit Prompt

Use the fuck-my-shit-mountain skill in **cost mode**.

Shared setup, coverage, report template, HTML, and lint rules live in `references/report-format.md`; load that reference before producing the report.

Focus on realistic cost risks from compute, storage, network, queues, background jobs, caches, observability, external APIs, and LLM/model usage.

## Audit Areas

### Unbounded Work
- User-controlled inputs can trigger expensive loops, queries, renders, exports, or batch jobs.
- Background tasks retry forever or fan out without a budget.
- Queues, caches, histories, logs, or traces grow without retention limits.
- Cron/scheduled jobs scan full datasets unnecessarily.
- Work is repeated instead of memoized or deduplicated.

### External API and LLM Costs
- LLM/API calls lack token, request, or concurrency budgets.
- No cache/deduplication for repeated prompts, embeddings, translations, or enrichments.
- Streaming or tool calls can loop without a hard stop.
- Model fallback silently upgrades to more expensive models.
- Errors trigger retries that multiply billable requests.

### Infrastructure Sizing
- Default resource limits are missing or too high.
- Autoscaling has no guardrails or scale-down path.
- Dev/test environments use production-sized resources.
- Container/serverless cold starts or concurrency settings create avoidable cost.
- Database indexes or query patterns create excessive read/write amplification.

### Observability and Storage Cost
- High-cardinality metrics labels explode time-series count.
- Logs/traces include large payloads or PII and lack sampling/retention.
- Artifacts, uploads, backups, and generated files have no lifecycle policy.
- Duplicate storage of raw and processed data has no cleanup or reconciliation.

### Cost Visibility
- No metrics or reports for per-tenant/user/workflow cost.
- No budgets, quotas, rate limits, or kill switches for expensive workflows.
- Costly feature flags can be enabled globally without approval.
- Billing-sensitive code has no tests for retry, deduplication, or limits.

## Rules

1. Only report cost risks with a plausible scale path or abuse path.
2. Include the cost driver: CPU, memory, storage, network, external API, model tokens, or operational toil.
3. Prefer caps, quotas, caching, deduplication, retention, and observability over premature optimization.
4. Treat cost controls as reliability controls when runaway cost can cause throttling or service shutdown.
5. For LLM/model costs, include token/request/concurrency boundaries where visible.


## Finding Format

Use the common fields in `templates/issue-card.md` and the format rules in `references/report-format.md`. Specialized evidence supplements those fields; it does not replace them.

Include these additional details when they help substantiate a finding:

- Subtype: UnboundedWork / ExternalApiCost / LLMCost / InfrastructureSizing / ObservabilityCost / CostVisibility
- Cost driver:
- Realistic cost scenario:
