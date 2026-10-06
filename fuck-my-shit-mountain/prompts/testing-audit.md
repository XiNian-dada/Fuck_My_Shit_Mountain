# Testing Audit Prompt

Use the fuck-my-shit-mountain skill in **testing mode**.

Shared setup, coverage, report template, HTML, and lint rules live in `references/report-format.md`; load that reference before producing the report.

Focus on whether the tests provide real confidence in the codebase.

## Audit Areas (see principles 8.1–8.5)

### Coverage Quality (not quantity)
- Critical paths without test coverage
- Error handling paths without test coverage
- Edge cases in input validation
- Boundary conditions
- Failure mode testing

### Test Types
- Unit test coverage of core logic
- Integration test coverage of external interfaces
- End-to-end test coverage of critical user flows
- Snapshot / golden file test quality
- Property-based or fuzz test coverage where appropriate

### Test Patterns
- Tests that only cover happy paths
- Tests that are over-mocked (testing mock behavior, not real behavior)
- Tests that assert implementation details (brittle)
- Tests that exist only for coverage metrics
- Tests that are flaky (non-deterministic)

### Missing Tests
- Regression tests for past bugs
- Concurrency / race condition tests
- Performance / benchmark tests
- Upgrade / migration tests
- Configuration permutation tests
- Security tests (auth bypass, injection, permission)

### Test Infrastructure
- CI test execution (speed, parallelism, ordering)
- Test data management (fixtures, factories, cleanup)
- Test isolation (shared state between tests)
- Test environment consistency
- Test reporting (what breaks, where, why)

## Grouping

Group recommendations into:

- **Must add** — without these, the project cannot be confidently released
- **Should add** — significant confidence gap
- **Nice to have** — incremental improvement
- **Not worth testing** — trivial, stable, or generated code


## Finding Format

Use the common fields in `templates/issue-card.md` and the format rules in `references/report-format.md`. Specialized evidence supplements those fields; it does not replace them.

Include these additional details when they help substantiate a finding:

- Behavior to test:
- Suggested test type: Unit / Integration / E2E / Property / Fuzz
- Minimal test case:
- Failure it would catch:
- Priority: Must add / Should add / Nice to have / Not worth testing
