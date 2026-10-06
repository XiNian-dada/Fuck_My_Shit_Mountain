# Design Principles Audit Prompt

Use the fuck-my-shit-mountain skill in **design mode**.

Shared setup, coverage, report template, HTML, and lint rules live in `references/report-format.md`; load that reference before producing the report.

Focus on practical violations of engineering principles from `rubrics/principles.md` that create correctness, maintainability, or release risk.

## Audit Areas

### Structure and Size Discipline
- SRP violations in functions, classes, modules, services, or components.
- Files/functions so large that behavior is hard to test or reason about.
- Excessive parameters, nesting, or cyclomatic complexity.
- Multiple unrelated reasons to change one unit.

### Coupling and Cohesion
- Modules that depend on too many unstable internal modules.
- Law of Demeter violations that couple callers to internal object shape.
- Concrete infrastructure dependencies inside high-level business logic.
- Interfaces that force clients to implement methods they do not use.

### Naming and Side Effects
- Names that hide mutation, I/O, network calls, persistence, or expensive work.
- Queries that also mutate state.
- Boolean traps and stringly typed state.
- Misleading abstractions that make failure modes surprising.

### Simplicity and Duplication
- Accidental duplication of real business rules.
- Over-engineered patterns without a current need.
- Abstractions with one implementation and no plausible second use.
- Complex generic code where a direct solution would reduce risk.

### Error and Boundary Design
- Invalid inputs traveling deep into the system before failing.
- Swallowed errors or lost error context.
- Generic public errors that prevent callers from handling failures.
- Missing fail-fast checks at external boundaries.

## Rules

1. Load `rubrics/principles.md` and cite exact principle IDs for findings.
2. Do not report principle violations that are only aesthetic.
3. Every design finding must explain the concrete change, bug, or test burden it creates.
4. Prefer local improvements over architecture rewrites.
5. A principle can be intentionally violated; accept it when the code documents and contains the tradeoff.


## Finding Format

Use the common fields in `templates/issue-card.md` and the format rules in `references/report-format.md`. Specialized evidence supplements those fields; it does not replace them.

Include these additional details when they help substantiate a finding:

- Principle: <principle name and ID from rubrics/principles.md>
- Why this creates risk:
