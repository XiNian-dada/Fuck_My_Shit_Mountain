# Frontend State Audit Prompt

Use the fuck-my-shit-mountain skill in **frontend-state mode**.

Shared setup, coverage, report template, HTML, and lint rules live in `references/report-format.md`; load that reference before producing the report.

Focus on frontend state management, component architecture, and UI data flow. This mode is for projects with a browser/client-side UI.

## Audit Areas

### Component Size
- Single-file components over 400 lines.
- Components that handle data fetching, transformation, rendering, and event handling.
- Components with too many responsibilities (SRP violation for UI).
- Render functions/methods over 100 lines.

### State Duplication and Sync
- Same data stored in multiple stores or component state.
- Manual sync between URL params, store state, and component local state.
- `props` that duplicate data already available in a store.
- State that is derived but stored instead of computed.

### Prop Drilling
- Props passed through 3+ levels of components without consumption.
- Components that accept 7+ props (suggests missing composition).
- "Wrapper" components that exist only to pass props through.

### Effect / Watch / Listener Proliferation
- `useEffect` / `watch` / `computed` chains that trigger each other.
- Effects that fetch data based on state that other effects modify.
- Missing cleanup in effects/subscriptions.
- Polling intervals that are not cleared on unmount.

### UI-Business Logic Coupling
- API calls inside component event handlers instead of store/services.
- Business rules (validation, formatting, filtering) duplicated in UI components.
- Navigation/routing logic mixed with data fetching.
- Components that directly mutate store state instead of calling actions.

### DOM-as-State
- Data read from DOM attributes or DOM text content instead of state/store.
- Hidden DOM elements used to store data for later access.
- CSS class names used as state flags.
- Refs used to store data that should be in state.

### Request State Management
- Loading/error states tracked manually per component instead of centralized.
- Race conditions in async requests (response order ≠ request order).
- No request deduplication (same request fired by multiple components).
- Optimistic updates without rollback on failure.

### Rendering Performance
- Large lists without virtualization.
- Components that re-render when unrelated state changes.
- Expensive computations in render functions without memoization.
- Unnecessary context subscriptions.

## Rules

1. Do not recommend a state management library migration unless the current approach is demonstrably causing bugs or severe maintenance pain.
2. Local component state is fine — not everything needs to be in a global store.
3. Consider the scale: patterns that are fine at 5 components may break at 50.


## Finding Format

Use the common fields in `templates/issue-card.md` and the format rules in `references/report-format.md`. Specialized evidence supplements those fields; it does not replace them.

Include these additional details when they help substantiate a finding:

- Subtype: ComponentSize / StateDuplication / PropDrilling / EffectChain / UIBusinessCoupling / DOMasState / RequestState / RenderPerf
- Why it creates maintenance risk:
- Recommended action: Split / Lift / Compute / Centralize / Debounce / Virtualize
