# Dependency Weight Audit Prompt

Use the fuck-my-shit-mountain skill in **dependency-weight mode**.

Shared setup, coverage, report template, HTML, and lint rules live in `references/report-format.md`; load that reference before producing the report.

Focus on whether dependencies are pulling their weight — not just known vulnerabilities, but whether each dependency is justified relative to the project's scale.

## Audit Areas

### Overweight Dependencies
- Large frameworks used for a tiny fraction of their capability.
- Library included for one utility function that could be inlined in 5 lines.
- Full-featured dependency where a lighter alternative exists.
- "Kitchen sink" dependencies that pull in transitive deps for unused features.
- Dependency that duplicates functionality of another included library.

### Dependency Count
- Total number of direct dependencies — is each one justified?
- Development dependencies that are never used in any script or build step.
- Dependencies that are only used in one file or one function.
- Dependencies added for a feature that was later removed (dead dependency).

### Transitive Dependency Risk
- Deep dependency trees (library → library → library → used for one call).
- Dependencies with no maintenance activity (stale, no recent releases).
- Dependencies with known CVEs that are not fixable by bumping version.
- Native bindings that complicate cross-platform builds.
- Dependencies with conflicting licenses.

### Build Toolchain Complexity
- Multiple build systems for the same project.
- Build scripts longer than the code they compile.
- Custom build tooling that could be replaced by standard toolchain features.
- Pre-build / post-install scripts that execute arbitrary code.
- Docker build stages that download unnecessary dependencies.

### Version Strategy
- No lockfile committed (cargo.lock, package-lock.json, yarn.lock).
- Overly permissive version ranges (`*`, `>=`, `^0`).
- Pinned versions with no upgrade cadence or policy.
- Duplicate versions of the same dependency (multiple versions in the tree).
- Git/submodule dependencies that are not pinned to a specific commit.

## Rules

1. Do not recommend removing a dependency unless the removal is realistic and reduces risk.
2. A "heavy" dependency is acceptable if it is used deeply and consistently.
3. Developer experience matters — a well-known library may be worth the weight for DX alone.
4. For each flagged dependency, check: can it be removed, replaced with a lighter alternative, or inlined?


## Finding Format

Use the common fields in `templates/issue-card.md` and the format rules in `references/report-format.md`. Specialized evidence supplements those fields; it does not replace them.

Include these additional details when they help substantiate a finding:

- Subtype: Overweight / Unused / DeadDependency / TransitiveRisk / ToolchainComplexity / VersionRisk
- Dependency:
- Why it is a risk:
- What it provides vs what the project actually needs:
- Recommended action: Keep / Inline / ReplaceWithLighter / Remove / AuditTransitives
- Build / test verification after removal:
