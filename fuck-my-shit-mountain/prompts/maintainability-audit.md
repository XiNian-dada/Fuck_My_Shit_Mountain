# Maintainability Audit Prompt

Use the fuck-my-shit-mountain skill in **maintainability mode**.

Shared setup, coverage, report template, HTML, and lint rules live in `references/report-format.md`; load that reference before producing the report.

Focus on maintainability, complexity, coupling, and design risk.

## Audit Areas

### Size & Structure (see principles 1.1–1.6)
- Files over 500 lines
- Functions over 50 lines
- Functions with deep nesting (4+ levels)
- Files with too many responsibilities — SRP violation (principle 1.1)
- Modules with unclear boundaries

### Complexity (see principles 1.5–1.6)
- Cyclomatic complexity hotspots (>10 paths)
- Functions with too many parameters (4+) — principle 1.4
- Functions with too many branches / conditions
- Complex conditional logic
- Deeply nested callbacks or promises
- Overuse of dynamic features (eval, reflection, metaprogramming)

### Coupling & Cohesion (see principles 2.1–2.6)
- Hidden dependencies between modules — principle 2.1
- Circular dependencies — principle 7.1
- Tight coupling to external libraries or frameworks — principle 2.4
- God objects / classes with too many responsibilities — SRP violation
- Shotgun surgery — one change requires touching many files
- Feature envy — a function that mostly uses data from another module — principle 2.3

### Duplication (see principle 4.1)
- Repeated logic that should be abstracted — DRY violation
- Copy-pasted code with minor variations
- Duplicated configuration or constants
- Parallel hierarchies that mirror each other

### Naming & Abstraction (see principles 3.1–3.5)
- Misleading names that do not reflect behavior — principle 3.1
- Names that hide side effects (e.g., `getX()` that mutates state) — principle 3.2
- Missing documentation on non-obvious behavior
- Documentation that contradicts the code
- Comments that explain "what" instead of "why"
- Boolean trap parameters — principle 3.5

### Design Patterns (see principles 4.2–4.3, 7.4–7.5)
- Business logic mixed with transport (HTTP, CLI, message queue) — principle 7.2
- Business logic mixed with persistence (SQL, file I/O) — principle 7.2
- Business logic mixed with UI rendering — principle 7.2
- Leaky abstractions that expose implementation details
- Premature abstraction — YAGNI violation (principle 4.2)
- Over-engineering — KISS violation (principle 4.3)
- Inheritance over composition — principle 7.4

### Changeability (see principles 4.1, 7.5)
- Code that is difficult to delete (too many callers, unclear ownership)
- Special-case logic scattered across the codebase
- Configuration scattered instead of centralized
- Default values duplicated across code paths — DRY violation
- Feature flags that are never cleaned up — YAGNI violation

## Rules

1. Do not recommend abstraction unless it removes real duplication, coupling, or confusion.
2. For each issue, include the risk of changing the code and the test needed before refactoring.
3. Prefer local improvements over architectural rewrites.


## Finding Format

Use the common fields in `templates/issue-card.md` and the format rules in `references/report-format.md`. Specialized evidence supplements those fields; it does not replace them.

Include these additional details when they help substantiate a finding:

- Why this affects maintainability:
- Risk of changing it:
- Local fix:
- Test needed before refactor:
