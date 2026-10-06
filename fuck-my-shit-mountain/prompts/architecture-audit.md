# Architecture Audit Prompt

Use the fuck-my-shit-mountain skill in **architecture mode**.

Shared setup, coverage, report template, HTML, and lint rules live in `references/report-format.md`; load that reference before producing the report.

Focus on module boundaries, dependency direction, layering, ownership, and whether the system shape supports safe change.

## Audit Areas

### Module Boundaries
- Modules with unclear ownership or overlapping responsibilities.
- Domain logic spread across UI, API handlers, database adapters, and scripts.
- "Utils" or "common" modules that hide unrelated behavior.
- Public APIs exposing implementation details.
- Cross-layer imports that bypass intended boundaries.

### Dependency Direction
- High-level policy depending directly on low-level infrastructure.
- Circular imports or package cycles.
- Feature modules depending on unstable internals from other features.
- Test-only architecture seams leaking into production design.
- Global singletons used instead of explicit dependencies.

### Data and State Ownership
- Multiple modules mutating the same state without a clear owner.
- Ambiguous source of truth for cached/derived data.
- Shared mutable state crossing async/thread/process boundaries.
- Persistence models reused as API or UI models where that creates coupling.
- State transitions implemented in multiple places.

### Boundary Contracts
- Missing contracts between layers, packages, services, or plugins.
- Implicit serialization formats or event payloads.
- Adapters that do validation/business logic inconsistently.
- Backward compatibility assumptions not documented or enforced.
- Runtime feature discovery where explicit interfaces would be safer.

### Evolution and Extensibility
- Adding a feature requires editing many unrelated modules.
- Extension points are too generic or too rigid.
- Architecture decisions are encoded only in tribal knowledge.
- Dead abstractions with one implementation and no realistic second use.
- Migration paths between old and new architecture are unclear.

## Rules

1. Judge architecture relative to project size and release stage.
2. Do not recommend rewrites unless local boundary repairs are clearly insufficient.
3. Cite concrete dependency paths, import cycles, state owners, or change scenarios.
4. Prefer small moves: introduce an interface, move validation to a boundary, split one module, or invert one dependency.
5. If a design is simple and works for the scale, do not over-architect it.


## Finding Format

Use the common fields in `templates/issue-card.md` and the format rules in `references/report-format.md`. Specialized evidence supplements those fields; it does not replace them.

Include these additional details when they help substantiate a finding:

- Subtype: ModuleBoundary / DependencyDirection / StateOwnership / BoundaryContract / EvolutionRisk
- Realistic change scenario:
