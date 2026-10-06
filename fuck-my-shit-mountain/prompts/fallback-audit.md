# Fallback Audit Prompt

Use the fuck-my-shit-mountain skill in **fallback mode**.

Shared setup, coverage, report template, HTML, and lint rules live in `references/report-format.md`; load that reference before producing the report.

Focus on "无异议兜底" — silent fallbacks, default values, empty catch blocks, compatibility branches, and defensive code that may be hiding real errors.

## Audit Areas

### Silent Fallbacks
- `||` / `or()` / `or_else()` default chains that silently activate.
- Fallback to hardcoded dev/empty values when config is missing.
- Optional/Maybe unwrapping with default that ignores the error.
- Default case in match/switch that returns a magic value without logging.

### Empty Catch / Ignored Errors
- Empty `catch {}` / `except: pass` blocks.
- `// TODO: handle error` with no follow-up.
- Return value of error-returning function discarded with `void` / `let _ =`.
- Errors mapped to `Ok(default)` instead of propagating.

### Compatibility Branches
- `if (isLegacy)` / `if (version < X)` branches in hot paths.
- Code paths that exist only to support old data formats indefinitely.
- Feature flags that are always enabled (or always disabled) with no cleanup plan.

### Silent Data Correction
- Input data silently mutated to fit schema (truncation, coercion, type casting).
- Validation that replaces invalid values with defaults instead of rejecting.
- Date/time parsing that silently assumes UTC/local when ambiguous.

### Defensive Guessing
- "Best effort" parsing that tries 3 formats and takes the first that doesn't crash.
- Network retry that silently succeeds on partial data.
- Auto-detection logic (language, encoding, timezone) with no user override.

## Rules

1. For each fallback, determine: **Should this fail fast, or is the fallback the correct behavior?**
2. If the fallback is correct, does it **log/warn/metric** so operators know it activated?
3. If the fallback is incorrect, recommend **fail-fast + clear error message**.
4. Distinguish between **defensive programming** (validates external input) and **defensive guessing** (hides bugs).
5. A fallback that activates silently and is never monitored is worse than a crash.


## Finding Format

Use the common fields in `templates/issue-card.md` and the format rules in `references/report-format.md`. Specialized evidence supplements those fields; it does not replace them.

Include these additional details when they help substantiate a finding:

- Subtype: SilentFallback / EmptyCatch / CompatibilityBranch / SilentCorrection / DefensiveGuess
- What it falls back from:
- Why the original path can fail:
- Is the fallback necessary? (Yes / No / Partial):
- If yes, is it monitored?:
- Recommended action: KeepWithAlert / FailFast / Remove / Restructure
