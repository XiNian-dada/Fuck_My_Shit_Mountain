# Evidence Rubric

## What Counts as Evidence

| Type | Example | Weight |
|------|---------|--------|
| Direct code observation | Line 42 calls `unwrap()` on a user-controlled value | Strong |
| Traceable control flow | Request path A → function B → branch C has no error handling | Strong |
| Runtime behavior | Test fails when input is empty | Strong |
| Config inspection | `app.config.secret = "hardcoded-dev-key"` | Strong |
| Dependency audit | Dependency v1.2.3 has CVE-2024-XXXX with public exploit | Strong |
| Comment indicating risk | `// TODO: this can deadlock under load` | Weak until verified against code or runtime behavior |
| Pattern inference | All handlers use `String::from_utf8_unchecked` | Medium |
| Structural inference | File is 3000 lines with 20 public functions | Medium |
| Missing pattern | No test file exists for `auth.rs` | Weak |
| Name-based inference | Function named `doStuff()` suggests unclear responsibility | Weak |

## Evidence Requirements by Severity

| Severity | Minimum Evidence |
|----------|-----------------|
| Critical | Direct code observation OR runtime behavior confirmation |
| High | Direct code observation OR traceable control flow |
| Medium | Direct code observation OR pattern inference |
| Low | Pattern inference OR structural inference |
| Info | Any |

## Evidence Requirements by Confidence

| Confidence | Minimum Evidence |
|------------|-----------------|
| High | Direct code observation or traceable control flow |
| Medium | Pattern inference or config inspection |
| Low | Structural inference or missing patterns |

## What Does NOT Count as Evidence

- "This looks bad" without explanation.
- "This is not idiomatic" — style alone is not evidence.
- "This might be slow" without identifying a bottleneck.
- "This is not scalable" without identifying the scaling limit.
- Personal preference about naming, formatting, or structure.
- Complaints about code not matching the reviewer's preferred paradigm.
- Assumptions about the developer's intent.

## Evidence Format

Every evidence block MUST include:

```
- File: <path with line numbers>
- Function / Module: <specific function or module name>
- Relevant behavior: <what the code actually does>
```

Optional but recommended:

```
- Input / state that triggers the behavior:
- Expected vs actual behavior:
- Test that demonstrates the issue:
```

Treat filenames, TODOs, line counts, and missing tools as leads. They do not establish a defect or its impact. Verify external vulnerability claims against authoritative advisories and the actual version/reachable usage before assigning severity.
