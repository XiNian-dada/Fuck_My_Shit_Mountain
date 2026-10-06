# [[PROJECT]] — Audit Report

**Modes:** [[MODES]]

**Date:** [[DATE]]

**Reviewer:** [[REVIEWER]]

**Scope / revision / worktree state:** [[RESOLVED_SCOPE]]

<!-- Localize visible headings/labels; preserve section and field markers. -->
<!-- section:executive-summary -->
## 1. Executive Summary

[[SUMMARY_WITH_RISKS_AND_LIMITS]]

<!-- section:score-dashboard -->
### Score Dashboard

<!-- One row per assessed score dimension; full includes all seven. Explain Not assessed rows. -->
| Dimension | Score | Grade | Coverage | Justification |
|---|---|---|---|---|
| [[SCORE_DIMENSION]] | [[SCORE_OR_NOT_ASSESSED]] | [[GRADE_OR_NOT_ASSESSED]] | [[SCORE_COVERAGE]] | [[JUSTIFICATION]] |
| Overall | [[OVERALL_OR_NOT_ASSESSED]] | [[OVERALL_GRADE_OR_NOT_ASSESSED]] | — | [[AGGREGATION_POLICY]] |

<!-- section:project-map -->
## 2. Project Map

[[STRUCTURE_ENTRY_POINTS_BOUNDARIES_AND_CRITICAL_FLOWS]]

**Commands and outcomes:** [[COMMANDS_AND_OUTCOMES]]

**Coverage limits:** [[EXCLUSIONS_AND_LIMITS]]

<!-- section:coverage -->
### Coverage Matrix

<!-- One row per selected audit dimension, identified by its canonical mode ID. -->
| Dimension | Coverage | Evidence inspected | Exclusions / limits |
|---|---|---|---|
| [[DIMENSION_ID]] | [[COVERAGE]] | [[EVIDENCE_INSPECTED]] | [[LIMITS]] |

<!-- section:statistics -->
### Finding Statistics

<!-- Preserve canonical severity values and column order; localize column labels. -->
| Severity | Count | Confirmed | Suspected |
|---|---|---|---|
| Critical | [[CRITICAL_COUNT]] | [[CRITICAL_CONFIRMED]] | [[CRITICAL_SUSPECTED]] |
| High | [[HIGH_COUNT]] | [[HIGH_CONFIRMED]] | [[HIGH_SUSPECTED]] |
| Medium | [[MEDIUM_COUNT]] | [[MEDIUM_CONFIRMED]] | [[MEDIUM_SUSPECTED]] |
| Low | [[LOW_COUNT]] | [[LOW_CONFIRMED]] | [[LOW_SUSPECTED]] |
| Info | [[INFO_COUNT]] | [[INFO_CONFIRMED]] | [[INFO_SUSPECTED]] |
| Total | [[TOTAL_COUNT]] | [[TOTAL_CONFIRMED]] | [[TOTAL_SUSPECTED]] |

<!-- section:top-risks -->
## 3. Top Risks

[[RANKED_RISKS_WITH_FINDING_IDS_OR_ZERO_FINDINGS_EXPLANATION]]

<!-- section:findings -->
## 4. Detailed Findings

<!-- Insert actual issue cards from issue-card.md, or an explicit no-findings explanation. -->
[[FINDING_CARDS_OR_NO_FINDINGS_EXPLANATION]]

<!-- Repeat this block once per selected dimension, replacing the marker with its canonical ID. -->
<!-- section:[[DIMENSION_ID]] -->
## 5. [[DIMENSION_LABEL]]

**Coverage:** [[COVERAGE]]

**Evidence inspected:** [[EVIDENCE_INSPECTED]]

**Exclusions / limits:** [[LIMITS]]

[[DIMENSION_ANALYSIS_OR_NOT_ASSESSED_REASON]]

| Finding ID | Finding | Severity | Status |
|---|---|---|---|
| [[FINDING_ID]] | [[FINDING_TITLE]] | [[SEVERITY]] | [[STATUS]] |

<!-- Remove the empty findings table when none exist. List only verified checks, with evidence. -->
[[VERIFIED_CHECKS_OR_NO_CHECKS_EXPLANATION]]

<!-- Optional: principles analysis when relevant; cite root finding IDs without recounting them. -->
[[PRINCIPLES_ANALYSIS_IF_APPLICABLE]]

<!-- section:fix-order -->
## 6. Recommended Fix Order

[[PRIORITIZED_FIXES_WITH_FINDING_IDS_OR_NO_ACTION_EXPLANATION]]

<!-- section:quick-wins -->
## 7. Quick Wins

[[LOW_COST_USEFUL_FIXES_WITH_FINDING_IDS_OR_NONE_EXPLANATION]]
