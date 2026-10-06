# Supply Chain and Reproducibility Audit Prompt

Use the fuck-my-shit-mountain skill in **supply-chain mode**.

Shared setup, coverage, report template, HTML, and lint rules live in `references/report-format.md`; load that reference before producing the report.

Focus on dependency provenance, build reproducibility, artifact integrity, CI pinning, release signing, SBOM, and supply-chain attack surface.

## Audit Areas

### Dependency Provenance
- Dependencies pulled from mutable branches, unpinned Git refs, or unauthenticated URLs.
- Internal package names vulnerable to dependency confusion.
- Install scripts, build scripts, or postinstall hooks execute unreviewed code.
- Transitive dependencies with unclear maintenance or ownership.
- Native binaries downloaded during install/build without verification.

### Lockfiles and Reproducibility
- Missing or ignored lockfiles for apps/services.
- Lockfiles not enforced in CI.
- Builds depend on current time, network, local machine paths, or ambient credentials.
- Generated artifacts differ across machines without explanation.
- Toolchain versions are not pinned or checked.

### CI/CD Integrity
- GitHub Actions or third-party actions pinned only to tags instead of SHAs where risk warrants SHA pinning.
- CI jobs run untrusted PR code with secrets.
- Release workflows can be triggered by unauthorized actors or branches.
- Build/test steps download scripts with curl | sh style patterns.
- Caches can poison later builds.

### Artifact Provenance
- Release artifacts are not signed or checksummed where users download them.
- No SBOM, provenance statement, or dependency inventory for public releases.
- Container images do not pin base images by digest.
- Build and release artifacts are produced by different code paths.
- Source archive does not match shipped binary/container.

### Package and Registry Hygiene
- Published packages lack ownership, two-factor requirements, or scoped registry config.
- Versioning can overwrite or shadow existing artifacts.
- Package contents include secrets, local files, test fixtures, or unnecessary build outputs.
- License conflicts or missing notices.

## Rules

1. Scale recommendations to distribution risk. Public packages and install scripts deserve stricter treatment than private prototypes.
2. Do not duplicate dependency-weight findings unless supply-chain risk is the core issue.
3. For each issue, identify attacker precondition and artifact/build surface.
4. Prefer pinning, verification, least privilege, reproducible builds, and provenance over broad toolchain swaps.
5. Treat secrets exposed to untrusted CI as Critical or High depending on blast radius.


## Finding Format

Use the common fields in `templates/issue-card.md` and the format rules in `references/report-format.md`. Specialized evidence supplements those fields; it does not replace them.

Include these additional details when they help substantiate a finding:

- Subtype: DependencyProvenance / Reproducibility / CIIntegrity / ArtifactProvenance / RegistryHygiene
- Affected surface:
- Attack precondition:
