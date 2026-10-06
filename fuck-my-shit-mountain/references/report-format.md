# Shared Report Contract

Use the request defaults in `SKILL.md`. This reference is the single source for report structure and format rules; focused prompts add audit evidence, not alternative required fields.

## Common Structure

Include these sections in order: Executive Summary, Score Dashboard, Project Map, Coverage Matrix, Finding Statistics, Top Risks, Detailed Findings, selected-dimension analysis, principles analysis when relevant, Recommended Fix Order, and Quick Wins.

Scale prose to the scope. A small PR can have short sections. Never fill an empty section with invented findings, fixes, or praise. With zero findings, show zero counts and explain the inspected scope; top risks, findings, fix order, and quick wins may be empty. A verified checklist contains only checks actually performed, with evidence; never reuse a template's example observations.

Per selected dimension, include coverage (High / Medium / Low / Not assessed), inspected evidence, and exclusions/limits. Use canonical mode IDs from prompt filenames for machine keys. Audit dimensions differ from the seven score dimensions in `rubrics/scoring.md`.

## Findings

Use `templates/issue-card.md` as the common contract in every mode. Required information:

| Machine field | Meaning |
|---|---|
| `severity` | Critical / High / Medium / Low / Info |
| `confidence` | High / Medium / Low |
| `category` | Primary audit dimension |
| `status` | Confirmed / Suspected |
| `affectedArea` | Affected module or surface |
| `evidence` | File and location, function/module, relevant behavior; runtime evidence if available |
| `problem` | Concrete defect or engineering risk |
| `userVisibleImpact` | Why it matters: user impact or concrete engineering cost |
| `failureScenario` | Realistic trigger and sequence of events |
| `minimalFix` | Smallest practical risk reduction |
| `regressionTestSuggestion` | Meaningful automated or manual regression verification |
| `estimatedEffort` | Estimate with uncertainty when needed |

Give each finding a unique ID (e.g. `F1`) and title. `betterLongTermFix`, subtype, attack path, concurrency interleaving, change type, and other mode-specific evidence are optional additions. They cannot substitute for required fields. Deduplicate root causes across categories; count each finding once.

## Markdown and stdout

Read `templates/audit-report.md` and `templates/issue-card.md`. Localize visible text freely, preserving these invisible markers in generated Markdown files:

- Before each required heading, `<!-- section:executive-summary -->`, `score-dashboard`, `project-map`, `coverage`, `statistics`, `top-risks`, `findings`, `fix-order`, or `quick-wins`.
- Before each dimension heading, `<!-- section:<canonical-mode> -->`, for example `<!-- section:concurrency -->`.
- Before each finding heading, `<!-- finding:F1 -->`.
- On each required field's first bullet line, `<!-- field:<machine-field> -->`. Example: `- 严重程度: <!-- field:severity --> High`. Keep enum values canonical; explain them in localized prose if helpful.

Use a statistics table with severity / count / confirmed / suspected columns in that order. Include all five canonical severity rows and a `Total` row, including zero rows. English and common Chinese labels are also understood, but markers avoid ambiguity in any language. For conversational stdout, markers may be omitted; verify equivalent content manually.

## HTML

Read `templates/audit-report.html`. Retain its CSS and reusable card structures, and repeat or remove dynamic rows/cards for actual data. Localize visible labels and the `lang` attribute. Do not preserve example text or force unused dimensions into the report.

- Use the same required section IDs as Markdown markers. Add one real element ID per selected dimension. Create navigation links only to real section IDs.
- Wrap each finding in `data-finding="F1"`. Put each required field's value inside an element with `data-field="<machine-field>"`; labels belong outside that element. For enums, that element contains only the canonical value.
- Each severity statistics card/row has `data-stat="High"`, `data-count="N"`, `data-confirmed="N"`, and `data-suspected="N"`. Include all five severity levels plus `data-stat="Total"`.
- Escape repository text and code before embedding them as HTML. Keep the document self-contained. Use stable IDs and attributes regardless of report language.
- Each dimension has its coverage note, findings table or no-findings explanation, and verified checklist. Inapplicable dimensions explain why they were Not assessed.

## JSON

Follow `templates/audit-report.json`, which is a schema, not a report to copy. Required sections include `dimensionSections`, `fixOrder`, and `quickWins`; use empty arrays when there is nothing to list. Key dimension analysis and coverage rows by canonical mode ID, such as `data-integrity`, rather than display labels or camelCase variants. Each dimension analysis has a `summary`; `verifiedChecks` is optional.

Use `null` for commitHash outside Git and for score/grade of Not assessed score dimensions. If no score dimension was assessed, overall score and grade are also `null`. Otherwise aggregate only assessed scores using `rubrics/scoring.md`. Each score includes `coverageConfidence`. A JSON finding's `userVisibleImpact` corresponds to the issue card's "Why it matters" field, and `problem` is required. Top risks and remediation entries reference existing finding IDs.

The standard-library linter validates the constraints used by this bundled schema and fails when it encounters unsupported schema constraints. It is not a general-purpose JSON Schema implementation.

## Validation

Run for every generated file, including both files in `both` mode:

```bash
python3 <skill-dir>/scripts/report_lint.py --modes <selected-modes> <report-file>
```

It checks supported format, placeholders, required sections/fields, selected dimensions, canonical enums, finding counts/statuses, HTML tags/navigation, JSON structure/references, and JSON score aggregation. It cannot prove evidence quality, complete coverage, or absence of every secret. Inspect those manually. Never echo sensitive matches while repairing errors. Record unavailable checks or unresolved validator failures honestly.
