# Testing Authenticity Audit Prompt

Use the fuck-my-shit-mountain skill in **testing-authenticity mode**.

Shared setup, coverage, report template, HTML, and lint rules live in `references/report-format.md`; load that reference before producing the report.

Focus on whether tests provide **real confidence** or just green checkmarks. This is not about coverage percentage — it is about whether the tests would catch real bugs.

## Audit Areas

### Over-Mocking
- Tests that mock everything except the exact function being tested.
- Mocks that return canned data and never exercise real behavior.
- Mock assertions that verify the mock was called (testing the mock framework, not the code).
- Mock setups that are more complex than the code under test.

### Testing Implementation, Not Behavior
- Tests that assert on internal state, private methods, or intermediate values.
- Tests that break on refactoring that does not change external behavior.
- Tests that know too much about how a function works internally.
- Snapshot tests that capture irrelevant output.

### Production Code Modified for Tests
- `if (isTest)` / `if (env === 'test')` branches in production code.
- Special constructors, setters, or config paths only used by tests.
- `#[cfg(test)]` / `if __name__ == '__main__'` that changes production behavior.
- Mock/injector frameworks that require production code to accept injected dependencies it otherwise would not need.

### Happy-Path-Only Tests
- Tests that only verify the success case.
- No tests for: invalid input, network error, auth failure, empty data, concurrent access.
- Error paths that return `Ok` are never tested with actual `Err` conditions.

### Brittle Tests
- Tests that depend on exact string matching of error messages.
- Tests that depend on timing, ordering, or random data.
- Tests that depend on specific dates or environment variables.
- Tests that fail when run in a different order.

### False Confidence
- 100% line coverage with no assertion on behavior (only that "no crash").
- Integration tests that start a server but never send realistic requests.
- Tests that pass with a broken implementation because the mock is too permissive.
- Property-based tests with trivial generators that never produce edge cases.

## Rules

1. A test that never fails is not a good test — it is a test that never catches bugs.
2. If production code has test-only branches, that is a design smell. Tests should exercise production paths, not create special ones.
3. Over-mocked tests test the mock, not the code. Reduce mock scope or write integration tests.
4. Snapshot tests are not free — each one is a maintenance liability.


## Finding Format

Use the common fields in `templates/issue-card.md` and the format rules in `references/report-format.md`. Specialized evidence supplements those fields; it does not replace them.

Include these additional details when they help substantiate a finding:

- Subtype: OverMocked / ImplDetail / ProdCodeForTest / HappyPathOnly / Brittle / FalseConfidence
- Why it produces false confidence:
- Recommended action: Rewrite / Delete / Keep but augment / Move to integration
- Suggested replacement test:
