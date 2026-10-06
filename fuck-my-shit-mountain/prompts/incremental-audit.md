# Incremental Audit

Review risks introduced or worsened by a change, including removed safeguards and broken callers. Load `references/report-format.md` for the common report contract. Incremental is a scope mode: alone it covers every focused dimension, or combine it with focused modes such as `incremental,security,concurrency`.

## Resolve Git Scope

Inspect Git status first. Validate requested refs and record the resolved commits, comparison type, merge base when applicable, and whether staged/unstaged/untracked changes are included. Never silently substitute another ref when the requested ref is missing. If this is not a Git repository, explain that an incremental comparison needs a supplied diff or a Git checkout.

Choose the comparison from the request:

- **PR / changes since divergence:** use `<base>...<head>`, defaulting head to `HEAD`. Example: `main...HEAD` compares the merge base with HEAD and excludes independent changes made on main. Determine the base from the request, PR metadata, or configured remote default branch. Ask if none is known; do not guess, switch branches, or fetch implicitly.
- **Explicit endpoint comparison:** preserve `<old>..<new>`. Example: `v1.2.0..HEAD` compares the release snapshot with HEAD. Two dots do not mean changes since branch divergence.
- **Single commit reference:** for committed changes since that snapshot, use `<commit>..HEAD`. If the request refers to a branch/PR, use the divergence comparison instead. Ask only if the distinction materially affects an ambiguous request.
- **Current worktree:** when requested, compare tracked content to the stated base (or HEAD) and inspect untracked files separately. `git diff HEAD --` includes staged and unstaged tracked changes; `git ls-files --others --exclude-standard -z` inventories untracked files. For a staged-only request, use `git diff --cached --`. Do not include unrelated existing edits in a committed PR review.

For committed comparisons, use the resolved range consistently:

```bash
git diff --name-status -z --find-renames <resolved-range> --
git diff --find-renames <resolved-range> --
git diff --numstat <resolved-range> --
```

Read the actual diff, not just filenames. Handle NUL-separated names without splitting paths at spaces or newlines. Renames retain their identity; inspect references and behavior rather than assuming every rename is a deletion plus an unrelated addition. Read deleted code from the relevant base snapshot. Empty diffs produce an explicit zero-change report, not a full audit.

## Trace Change Impact

- Check new vulnerabilities, failure paths, races, persistence and privacy risks.
- Inspect deleted validation, error handling, synchronization, and tests.
- Follow unchanged callers and dependencies as needed to understand the affected contract.
- Check dependency/configuration changes, schema migrations, and public API compatibility.
- Evaluate whether existing tests cover the changed behavior. Missing new test files alone is not a finding.
- Report pre-existing issues only when the change makes them worse; explain the causal link to the diff.
- Set severity by demonstrated impact and reachable conditions, not merely by number of callers or lines changed.

Keep the findings proportional to demonstrated risks. A small change may have a large impact, but it does not justify unrelated repository-wide findings.

## Finding Evidence

Use `templates/issue-card.md`. Add the changed file/function, relevant base and head behavior, diff location, change type (Added / Modified / Deleted / Renamed), and related unchanged callers. Show what changed and why the change introduces or worsens the risk.

## Report Additions

Include a change summary with the resolved scope, changed file count, added/deleted lines, and any worktree exclusions. Derive numbers from the actual Git output; do not guess feature/bug-fix categories from filenames. Describe test coverage gaps and risk changes only when they were inspected.

If the user requests a merge recommendation, tie it to findings and coverage: request changes for demonstrated blocking risks, approve with comments for non-blocking issues, or state insufficient evidence when important checks are missing. An empty finding list alone does not establish that merging is safe. The recommendation is advisory; do not merge or post comments unless separately authorized.
