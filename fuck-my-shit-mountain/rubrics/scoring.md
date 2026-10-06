# Scoring Rubric

Scores summarize evidence-backed engineering quality within the audited scope. Higher is better, from 0.0 to 10.0. They are judgments, not mechanical deductions for each finding, and they do not certify a release as safe.

## Score Dimensions

Audit modes and score dimensions are different. Map findings and coverage to these seven dimensions:

| Score dimension | Measures | Mapped modes |
|---|---|---|
| Security | Auth, injection, secrets, dependencies, privacy and AI/tool boundaries | security, type-safety, configuration, privacy, supply-chain, ai-safety |
| Stability | Failure handling, state consistency, fallback, data correctness and concurrency | stability, concurrency, fallback, observability, configuration, data-integrity, privacy, ai-safety |
| Performance | Realistic load, memory, I/O, contention and external resource cost | performance, concurrency, dependency-weight, cost, ai-safety |
| Testing | Confidence in critical behavior, regression protection and evals | testing, testing-authenticity, concurrency, accessibility, ai-safety |
| Maintainability | Architecture, complexity, change cost, docs, state and APIs | architecture, maintainability, documentation, frontend-state, backend-api, code-consistency, comment-coverage, accessibility |
| Design | Responsibility, abstraction, type safety and boundary design | architecture, design, type-safety, concurrency, accessibility |
| Release | CI/CD, upgrades, rollback, configuration, migrations and provenance | release, dependency-weight, observability, configuration, data-integrity, documentation, supply-chain, cost, privacy |

For full audits, include all seven rows. For focused audits, score relevant dimensions only when evidence supports them; one selected mode can map to multiple scores. Mark inapplicable or inaccessible score dimensions Not assessed with a reason, never as zero.

## Anchors and Grades

| Score | Grade | Evidence-based interpretation |
|---|---|---|
| 9.0–10.0 | S | Strong quality in the inspected scope; isolated minor issues at most |
| 7.0–8.9 | A | Real but contained risks; local improvements needed |
| 5.0–6.9 | B | Significant recurring risks requiring deliberate work |
| 3.0–4.9 | C | Serious structural or reliability weaknesses |
| 1.0–2.9 | D | Severe, pervasive failures in this dimension |
| 0.0–0.9 | F | Fundamentally unreliable within the assessed scope |

Judge impact, exposure, safeguards, intensity, and distribution together. A single Critical issue can block release regardless of the overall grade. Line count and personal style do not determine a score.

Each score has a justification referencing the strongest evidence and a coverage confidence. Zero findings permits 10.0 only with High coverage; Medium/Low coverage must explain its limits and cannot support a high-confidence clean conclusion. A high score means strong evidence in the inspected scope, not proof of perfection. Finding confidence and coverage confidence remain separate.

## Overall Score

Default to the arithmetic mean of assessed score dimensions, rounded to one decimal place. Exclude Not assessed dimensions from both numerator and denominator. If none were assessed, overall is Not assessed; JSON uses null for score and grade.

Use weighted aggregation only when the user requests a weighting policy. Record weights for exactly the assessed score dimensions and explain the policy; weights are nonnegative with a positive total. Normalize them over assessed dimensions:

`overall = round(sum(score_i * weight_i) / sum(weight_i), 1)`

Do not infer new weights silently from a framework or change the policy between reports used for trends. A focused or incremental scope is not directly comparable to a full repository audit; retain scope and coverage with historical scores.

## Display

Show one decimal place without rounding to improve a grade. Assign the grade from the displayed score using the ranges above. Markdown may use a ten-character bar, filling the nearest whole number of blocks; a displayed 3.5 uses four filled blocks. Not assessed has no numeric bar. HTML uses the same score direction. In JSON, score and grade are null for Not assessed rows; otherwise both are required and must agree.
