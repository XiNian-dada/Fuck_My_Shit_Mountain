# Release Audit Prompt

Use the fuck-my-shit-mountain skill in **release mode**.

Shared setup, coverage, report template, HTML, and lint rules live in `references/report-format.md`; load that reference before producing the report.

Focus on whether this project can be safely released, installed, upgraded, and rolled back.

## Audit Areas (see principles 9.1–9.3: Configuration & Environment)

### CI/CD Pipeline
- What checks run in CI? (lint, typecheck, test, build, security scan)
- Are there gates before merge? Before release?
- Build matrix (OS, architecture, language version)
- Artifact caching and reproducibility
- CI speed — does it discourage frequent releases?

### Versioning
- Version scheme (semver, date-based, commit-based)
- Version defined where and how
- Pre-release handling (alpha, beta, rc)
- Version bump automation
- Breaking change detection
- Changelog generation

### Build & Artifacts
- Build script correctness and determinism
- Dependency vendoring or lockfile
- Artifact naming and storage
- Checksum / signature generation
- SBOM generation
- Binary / package provenance

### Installation
- Install script safety (no curl-bash without verification)
- Package manager registration (npm, cargo, pip, docker)
- Minimum supported version documentation
- Dependency resolution and conflicts
- First-run experience

### Upgrade Path
- Data migration (schema, config, state format)
- Backward compatibility period
- Deprecation policy
- Config file format migration
- State / database migration rollback

### Rollback
- Can a release be rolled back?
- Is the previous artifact available?
- Data migration reversibility
- Config migration reversibility
- Rollback testing

### Deployment
- Dockerfile quality (multi-stage, layer caching, non-root user)
- Service definition (systemd, launchd, kubernetes)
- Environment variable configuration
- Health check endpoint
- Startup probe, readiness probe, liveness probe
- Resource limits

### Compatibility
- API versioning strategy
- Breaking change communication
- Documentation of compatibility guarantees
- Deprecation notice period

## Rules

1. Focus on practical release risks, not hypothetical edge cases.
2. For each issue, include the user impact and a specific validation step.

## Finding Format

Use the common fields in `templates/issue-card.md` and the format rules in `references/report-format.md`. Specialized evidence supplements those fields; it does not replace them.

Include these additional details when they help substantiate a finding:

- Release risk:
- User impact:
- Better release process:
- Validation step:
