# Accessibility and UX Correctness Audit Prompt

Use the fuck-my-shit-mountain skill in **accessibility mode**.

Shared setup, coverage, report template, HTML, and lint rules live in `references/report-format.md`; load that reference before producing the report.

Focus on whether browser/client UI workflows remain usable, understandable, and correct across keyboard, screen reader, responsive, loading, empty, and error states.

## Audit Areas

### Semantic Structure
- Interactive elements built from non-semantic elements without roles or keyboard handling.
- Inputs without labels or accessible names.
- Icon-only controls without accessible labels.
- Headings, landmarks, dialogs, tabs, and menus not represented semantically.
- Status messages not announced to assistive technology.

### Keyboard and Focus
- Critical workflows unavailable by keyboard.
- Focus lost, trapped incorrectly, or not restored after modal/route changes.
- Roving tab index, menu navigation, or tab panels implemented incorrectly.
- Keyboard shortcuts conflict with browser or assistive technology behavior.
- Disabled/loading states leave focus on unusable controls.

### Visual and Responsive Correctness
- Text, controls, or overlays overlap on realistic viewport sizes.
- Contrast, focus ring, hover-only affordances, or disabled state is unclear.
- Dynamic content shifts layout in a way that causes wrong clicks.
- Touch targets are too small or too close.
- Zoom/text scaling breaks workflows.

### Error, Empty, and Loading States
- Forms do not associate validation errors with fields.
- Async failures leave stale data or disabled controls.
- Loading states hide the user's current task or cause duplicate submissions.
- Empty states lack the actionable controls needed to recover.
- Error messages are not specific enough for users to fix input.

### UX Data Flow Correctness
- UI displays state different from persisted/server state.
- Optimistic updates do not roll back on failure.
- Request cancellation or route changes show wrong data.
- Client-side validation disagrees with backend validation.
- Critical actions lack confirmation or undo where the domain requires it.

## Rules

1. This mode applies to browser/client UI projects. For non-UI projects, mark Not assessed with evidence.
2. Do not report generic accessibility advice; tie every finding to a real workflow.
3. Prefer semantic HTML and small component fixes over adding heavy UI libraries.
4. When practical, verify with browser inspection, keyboard flow, or accessibility tree evidence.
5. Include a regression test suggestion using the project's UI test stack when available.


## Finding Format

Use the common fields in `templates/issue-card.md` and the format rules in `references/report-format.md`. Specialized evidence supplements those fields; it does not replace them.

Include these additional details when they help substantiate a finding:

- Subtype: SemanticStructure / KeyboardFocus / ResponsiveVisual / ErrorState / LoadingState / UXStateCorrectness
- Affected workflow:
- User-visible failure scenario:
