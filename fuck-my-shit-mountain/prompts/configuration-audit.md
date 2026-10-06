# Configuration Audit Prompt

Use the fuck-my-shit-mountain skill in **configuration mode**.

Shared setup, coverage, report template, HTML, and lint rules live in `references/report-format.md`; load that reference before producing the report.

Focus on configuration correctness, validation, environment separation, feature flag hygiene, and safe runtime defaults.

## Audit Areas

### Configuration Schema and Validation
- Required configuration values not validated at startup.
- Config parsed as raw strings without type/schema validation.
- Invalid values fail later during request handling instead of failing fast.
- Config defaults are hidden across multiple files.
- No clear precedence between file, environment variable, CLI flag, and runtime override.

### Safe Defaults
- Development defaults usable in production.
- Empty or placeholder secrets accepted.
- Missing URLs, credentials, ports, or paths silently replaced with unsafe defaults.
- Debug, permissive CORS, verbose logging, or test mode enabled by default.
- Timeouts, limits, pool sizes, and retry counts missing or unbounded.

### Environment Separation
- Production and development differ by code path instead of configuration values.
- Environment detection relies on brittle string matching.
- Test-only config branches can affect production behavior.
- Local-only assumptions leak into container, cloud, or CI deployment.
- Config values depend on machine-specific absolute paths.

### Secrets and Sensitive Config
- Secrets stored in committed files, templates, logs, or generated reports.
- Secret values passed through command-line arguments or visible process lists.
- Config reload or debugging endpoints expose sensitive values.
- Rotation is impossible without restart or redeploy where the project requires live rotation.
- No separation between secret config and non-secret config.

### Feature Flags and Runtime Switches
- Flags with no owner, expiry date, or cleanup plan.
- Flags that are always true/false in all known environments.
- Flag combinations that create untested behavior.
- Runtime switches bypass authorization or validation.
- Flag state changes are not logged or auditable.

### Config Documentation
- README/docs list values that no longer match code.
- Missing examples for required production configuration.
- No documented config migration path.
- No explanation for non-obvious limits, timeouts, or resource caps.

## Rules

1. Required config must fail at startup with a clear error, not degrade later.
2. Treat unsafe production defaults as release or security risks depending on impact.
3. Do not complain about simple config files in small projects unless the simplicity hides real risk.
4. Validate docs against actual config parsing code.
5. For each issue, include the exact config key/value path and the failure mode.


## Finding Format

Use the common fields in `templates/issue-card.md` and the format rules in `references/report-format.md`. Specialized evidence supplements those fields; it does not replace them.

Include these additional details when they help substantiate a finding:

- Subtype: SchemaValidation / UnsafeDefault / EnvironmentSeparation / SecretConfig / FeatureFlag / ConfigDocs
