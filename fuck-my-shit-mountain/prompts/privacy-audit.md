# Privacy and Data Governance Audit Prompt

Use the fuck-my-shit-mountain skill in **privacy mode**.

Shared setup, coverage, report template, HTML, and lint rules live in `references/report-format.md`; load that reference before producing the report.

Focus on personal data handling, data minimization, retention, deletion, export, logging, access boundaries, and privacy-relevant governance.

## Audit Areas

### Data Inventory and Classification
- PII or sensitive data collected without a clear purpose.
- Personal data fields stored without classification or ownership.
- Sensitive fields copied into analytics, logs, caches, queues, or exports.
- Test fixtures or examples contain realistic personal data.
- Derived identifiers can re-identify users.

### Data Minimization
- Collecting or persisting fields not needed for current behavior.
- Sending full records where only IDs or aggregates are needed.
- Retaining raw payloads after extraction.
- Third-party integrations receive unnecessary user data.
- Debug/admin tools expose full records by default.

### Consent, Access, and Purpose Boundaries
- Privacy-sensitive processing has no user/account-level gate.
- Internal roles can access more data than their job requires.
- Admin or support tooling lacks audit logs.
- Data is reused across features without a clear purpose boundary.
- Tenant/account boundaries are not enforced in privacy-sensitive queries.

### Retention, Deletion, and Export
- No retention period for logs, events, uploads, or backups.
- Delete requests do not remove derived data, caches, queues, or search indexes.
- Export misses important user data or includes other users' data.
- Backups make deletion guarantees misleading.
- Retention config differs from documented policy.

### Privacy in Logs and Telemetry
- PII appears in logs, traces, metrics labels, crash reports, or error responses.
- High-cardinality labels contain user identifiers.
- Correlation IDs can be linked to personal data without controls.
- Third-party telemetry SDKs send sensitive context by default.

## Rules

1. Privacy findings must identify the personal or sensitive data involved.
2. Do not cite legal compliance obligations unless the project explicitly targets that regime; describe engineering risk instead.
3. Treat PII in logs as both privacy and security risk.
4. Prefer data minimization, redaction, access control, retention config, and audit trails over broad rewrites.
5. If no personal data is processed, mark the mode Not assessed or Info with evidence.


## Finding Format

Use the common fields in `templates/issue-card.md` and the format rules in `references/report-format.md`. Specialized evidence supplements those fields; it does not replace them.

Include these additional details when they help substantiate a finding:

- Subtype: DataInventory / Minimization / AccessBoundary / Retention / Deletion / Export / TelemetryPrivacy
- Affected data:
- Realistic privacy failure scenario:
