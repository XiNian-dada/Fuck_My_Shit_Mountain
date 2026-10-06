# Type Safety Audit Prompt

Use the fuck-my-shit-mountain skill in **type-safety mode**.

Shared setup, coverage, report template, HTML, and lint rules live in `references/report-format.md`; load that reference before producing the report.

Focus on whether the type system is providing real safety guarantees or is being bypassed through escape hatches.

## Audit Areas

### Unsafe and Escape Hatches
- `unsafe` blocks — are they justified? Do they have safety comments?
- `any` / `unknown` casts without narrowing.
- Type assertions (`as Type`, `as!`, `unchecked_cast`) — are they provably correct?
- Non-null assertions (`!`, `unwrap()`, `!!`) — can the value actually be null?
- `// @ts-ignore` / `// @ts-expect-error` — how many, what are they hiding?

### Input Boundary Weakness
- API request bodies typed as `any` / `serde_json::Value` / `Dictionary` without validation.
- Config files parsed without schema validation.
- User input accepted as the target type without parsing/validation step.
- Database query results cast to model types without runtime verification.

### Output Boundary Leakage
- Internal types exposed in public API responses.
- Sensitive fields not excluded from serialization.
- Error types that leak internal state (stack traces, DB queries, IPs).

### State Representation
- Boolean parameters that create confusing call sites (boolean trap — principle 3.5).
- Stringly-typed values that should be enums or sum types.
- `null` / `undefined` / `nil`/ `None` used to represent "not found" vs "error" vs "not initialized".
- Shared mutable state without type-level synchronization guarantees.
- Magic strings/numbers used where constants or enums would constrain values.

### Error Type Quality
- Generic error types (`Box<dyn Error>`, `Exception`, `string`) in public APIs.
- Errors that lose the original cause (no wrapping, no context).
- Catch-all error handlers that return a generic 500 without details.
- Missing `#[non_exhaustive]` on public error enums.

### Generics and Trait Bounds
- Overly permissive generic bounds (accepting `Any`/`Object` when concrete type is known).
- Traits with too many methods (ISP violation).
- Associated types that leak implementation details.

## Rules

1. Every `unsafe` block must have a safety comment explaining why it is safe.
2. Every type assertion must be provably correct in all code paths.
3. If the language supports sum types / enums / ADTs, prefer them over `null` + boolean flags.
4. External input must have a validation boundary — typed is not the same as validated.


## Finding Format

Use the common fields in `templates/issue-card.md` and the format rules in `references/report-format.md`. Specialized evidence supplements those fields; it does not replace them.

Include these additional details when they help substantiate a finding:

- Subtype: UnsafeBlock / TypeAssertion / InputBoundary / OutputLeak / BooleanTrap / StringlyTyped / ErrorType
- Why it weakens safety guarantees:
- Minimal fix (tighter type):
