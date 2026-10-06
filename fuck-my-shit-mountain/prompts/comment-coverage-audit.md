# Comment Coverage Audit Prompt

Use the fuck-my-shit-mountain skill in **comment-coverage mode**.

Shared setup, coverage, report template, HTML, and lint rules live in `references/report-format.md`; load that reference before producing the report.

Focus on documentation quality, comment coverage of public APIs, stale/misleading comments, and the balance between useful documentation and unnecessary noise.

## Audit Areas

### Public API Documentation
- Public functions/types/constants without doc comments (where the language/ecosystem expects them).
- Missing module-level documentation (no module overview, no purpose statement).
- API surfaces that lack examples or usage guidance.
- Parameters or return values not documented (especially non-obvious ones like boolean flags, magic numbers, or error conditions).

### Stale / Misleading Comments
- Comments that describe behavior no longer true (refactored code, changed assumptions).
- "TODO" / "FIXME" / "HACK" / "XXX" comments that are years old with no associated issue or plan.
- Comments that lie (describe one thing, code does another).
- Commented-out code blocks without explanation of why they're kept.
- Outdated file headers, copyright dates, or author lines.

### Over-commenting / Noise
- Comments that simply restate the code in English (`i += 1  // increment i`).
- Comment headers for trivial sections (`// Getters`, `// Constructor`).
- Change log comments in file headers (`2024-01-01: fixed bug` — that's what git is for).
- Comments that explain "what" instead of "why".

### Module / Package Documentation
- Missing README or module-level docs for key packages.
- Missing architecture decision records (ADR) for non-obvious design choices.
- Missing setup/configuration documentation for development environment.
- No documented error handling strategy or conventions.

### Inline Comment Quality
- Comments that don't add context (explaining trivial code, missing explanation of non-trivial code).
- Magic numbers/strings without explanation.
- Complex algorithms or business rules without rationale comments.
- Safety invariants (lock ordering, memory ownership, thread safety assumptions) not documented.

### Self-Documenting Code
- Code so convoluted that even a well-written comment can't save it — consider this a finding.
- Functions with 7+ parameters that need a novel to explain what each does.
- Names so misleading that they contradict what the code actually does.

## Rules

1. A missing doc comment on every trivial getter/setter is not a finding. A missing doc on a public API that has unclear preconditions or side effects is.
2. Prioritize stale/misleading comments over missing ones — wrong docs are worse than no docs.
3. Consider the project's language ecosystem norms (Rust expects doc comments on pub items, Python less so).
4. Flag commented-out code only if it's extensive (5+ lines) or has been there for multiple commits.


## Finding Format

Use the common fields in `templates/issue-card.md` and the format rules in `references/report-format.md`. Specialized evidence supplements those fields; it does not replace them.

Include these additional details when they help substantiate a finding:

- Subtype: MissingDoc / StaleComment / NoiseComment / MissingModuleDoc / PoorInlineComment / NotSelfDocumenting
- Why this matters:
- Impact on maintainability or onboarding:
