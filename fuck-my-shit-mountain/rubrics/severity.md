# Severity Rubric

Determine severity from demonstrated impact, likelihood, exposure, and existing safeguards. Examples below require those conditions; a scanner label, missing test/tool, code size, or naming pattern alone does not determine severity. Public endpoints, intentionally handled failures, and non-sensitive example values are not automatically vulnerabilities.

## Critical

- Remote code execution or privilege escalation.
- Exposed valid production credentials or secrets enabling significant unauthorized access.
- Vulnerable dependency with known exploit in production use.
- Data loss or corruption on normal operation.
- Complete service unavailability on a realistic failure path.
- Missing authentication on a production endpoint that exposes privileged actions or sensitive data without another effective boundary.

## High

- Authorization bypass or privilege escalation within the application.
- SQL/command injection with realistic attack surface.
- Unhandled panic/crash on expected input or state.
- Deadlock or live-lock under normal concurrency.
- Memory leak that exhausts resources within hours.
- Persistent data inconsistency on partial failure.
- Missing input validation on security-sensitive paths.
- Breaking change without version bump in a published package.
- A demonstrated high-impact regression risk on a critical path that existing tests cannot detect; explain the behavior and confidence gap.

## Medium

- XSS or open redirect with realistic constraints.
- Error message that leaks internal state to the client.
- Retry without backoff or circuit breaker.
- No timeout on an external call.
- Unbounded collection growth under normal load.
- Large function or module with unclear responsibility.
- Missing error handling in a non-critical path.
- Flaky test that fails CI non-deterministically.
- Slow query on a table expected to grow.
- Duplicated logic that increases maintenance cost.

## Low

- Inconsistent conventions that create demonstrated maintenance cost without affecting correctness.
- Missing comments on non-obvious logic.
- Minor logging inconsistency.
- Untested edge case in a low-risk path.
- Dead code that is not actively harmful.
- Minor documentation inaccuracy.
- Warning-level linter findings.

## Info

- Observations that are not risks but may be relevant context.
- Architecture notes for future consideration.
- Patterns that may become risks under different scale.
- Suggestions that do not meet threshold for any severity level.
