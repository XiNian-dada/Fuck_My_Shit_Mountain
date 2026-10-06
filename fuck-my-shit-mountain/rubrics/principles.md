# Software Engineering Principles Rubric

A catalog of investigation signals for design and maintainability. Numeric thresholds are heuristics, not automatic findings. Verify responsibility, reachable behavior, safeguards, and concrete change cost before reporting a violation. Use `severity.md` as the sole severity authority; size, naming, or a principle label alone cannot justify High or Critical.

---

## 1. Structure & Size Discipline

### 1.1 Single Responsibility (SRP)
> A module/class/function should have one reason to change.

- **Detection:** Count distinct responsibilities in one file/function. If a function parses input, validates auth, queries DB, and formats response — it violates SRP.
- **Threshold:** >1 clear responsibility per function; >3 per class/module.
- **Example:** A 400-line `handleRequest` that does auth, routing, business logic, serialization, and logging.

### 1.2 File Size Limit
> A source file should not exceed reasonable size limits.

- **Detection:** Count lines of code (excluding blank lines and imports).
- **Threshold:** >500 lines → inspect cohesion and navigation cost; >1000 lines → prioritize that inspection.
- **Exception:** Generated code, data tables, enum definitions.

### 1.3 Function/Method Size
> A function should fit in a screenful of code.

- **Detection:** Count lines within function body.
- **Threshold:** >50 lines → inspect branching and testability; >100 lines → prioritize that inspection.

### 1.4 Parameter Count
> A function should have few parameters.

- **Detection:** Count formal parameters.
- **Threshold:** >4 parameters → inspect call-site ambiguity; >7 → inspect whether grouping would clarify actual domain concepts.
- **Exception:** Constructor dependency injection.

### 1.5 Nesting Depth
> Deep nesting indicates complexity.

- **Detection:** Measure maximum indentation level within a function.
- **Threshold:** >4 levels → flag; >7 → High.

### 1.6 Cyclomatic Complexity
> Too many independent paths through a function.

- **Detection:** Count branches (if, else, case, loops, catch, logical operators).
- **Threshold:** >10 → flag; >20 → High.

---

## 2. Coupling & Cohesion

### 2.1 Low Coupling
> Modules should depend on few other modules, and only on stable ones.

- **Detection:** Count imports/requires/includes that reference project-internal modules.
- **Threshold:** >10 internal imports → flag.
- **Form:** A utils/helpers module imported by 30+ files.

### 2.2 High Cohesion
> Elements within a module should be functionally related.

- **Detection:** If a module contains unrelated functionality (e.g., string utilities + network calls + config parsing), it has low cohesion.
- **Threshold:** Module name cannot describe all its contents.

### 2.3 Law of Demeter (Principle of Least Knowledge)
> A unit should not know about the internal structure of objects it depends on.

- **Detection:** Chained method/property access like `a.b.c.d()` or `getX().getY().doZ()`.
- **Threshold:** >2 dots past the receiver (excluding fluent APIs and builders).

### 2.4 Dependency Inversion (DIP)
> Depend on abstractions, not concretions.

- **Detection:** High-level module directly instantiates or references a low-level concrete implementation.
- **Threshold:** Database driver, file system, or network library directly used in business logic.

### 2.5 Interface Segregation (ISP)
> Clients should not depend on interfaces they do not use.

- **Detection:** A struct/class implements interface methods that throw `NotImplemented` / `panic!` / `return null`.
- **Threshold:** >1 method is a no-op or throws.

### 2.6 Stable Dependencies Principle
> Depend in the direction of stability.

- **Detection:** An unstable module (frequently changed) is depended upon by many other modules.
- **Threshold:** A module with >5 dependents and >10 commits/changes in last month.

---

## 3. Naming & Abstraction

### 3.1 Principle of Least Surprise
> Code should behave as its name and signature imply.

- **Detection:** `getX()` that mutates state; `save()` that also sends email; `isValid()` that has side effects.
- **Threshold:** Any violation.

### 3.2 Command-Query Separation (CQS)
> A function should be either a command (mutates state, returns void) or a query (returns data, no side effects), not both.

- **Detection:** Function that both mutates state AND returns a value (unless it's a well-known pattern like `pop()`).
- **Threshold:** Any violation.

### 3.3 Tell, Don't Ask
> Tell an object what to do rather than asking for its data and operating on it externally.

- **Detection:** Code that calls getters on an object then uses that data in conditionals or computations.
- **Threshold:** Repeated pattern across >3 locations.

### 3.4 Meaningful Names
> Names should reveal intent and avoid misleading abbreviations.

- **Detection:** Single-letter names (except loop counters), cryptic abbreviations (`d`, `tmp`, `data`, `val`, `handleStuff`), misleading names (`String fileName` that actually contains a URL).
- **Threshold:** Flag any obviously misleading name. Flag uninformative names in public APIs.

### 3.5 Boolean Trap
> Boolean parameters create confusing call sites.

- **Detection:** Function parameter of type `bool` that controls behavior branching.
- **Threshold:** Any `bool` parameter that is not a simple flag for an optimization/cache.
- **Fix:** Replace with enum or separate functions.

---

## 4. Code Quality

### 4.1 DRY (Don't Repeat Yourself)
> Every piece of knowledge must have a single, unambiguous representation.

- **Detection:** Identical or near-identical code blocks >3 lines long appearing in multiple places.
- **Threshold:** >2 occurrences of identical logic.
- **Important:** Distinguish accidental duplication (coincidental) from essential duplication (same logic but different domains). Only flag the former.

### 4.2 YAGNI (You Ain't Gonna Need It)
> Do not add functionality until it is necessary.

- **Detection:** Unused parameters, dead code paths, abstraction layers with only one implementation, generic configuration for features that do not exist.
- **Threshold:** Code that is compiled/shipped but never used.

### 4.3 KISS (Keep It Simple, Stupid)
> Simple solutions are better than complex ones.

- **Detection:** Unnecessary design patterns (Factory for one implementation, Visitor for 2 types), over-abstracted code (one-liner wrapped in a class hierarchy), complex configuration DSL for simple behavior.
- **Threshold:** Flag when a simpler alternative is obvious and reduces total code by >30%.

### 4.4 Fail-Fast
> Fail as early and as clearly as possible.

- **Detection:** Functions that accept invalid input and pass it deeper before eventually failing; missing null/empty/validity checks at public API boundaries; silent fallbacks that mask errors.
- **Threshold:** Any case where an invalid input propagates >3 layers before detection.

### 4.5 Defensive Programming — Appropriate Level
> Validate inputs, but don't over-defend against internal inconsistencies.

- **Detection:** Assertions that check internal invariants at every call site (suggesting lack of trust in own code); vs. missing validation on external input.
- **Threshold:** Flag missing validation on external input (High). Flag redundant internal checks (Low).

### 4.6 Principle of Least Privilege
> Code should have only the permissions it needs.

- **Detection:** Global mutable state accessible by all modules; functions that accept more data than they need; overly broad API exposure (`pub` everything, `export *`).
- **Threshold:** Any public API surface that is not needed by external consumers.

---

## 5. State & Side Effects

### 5.1 Immutability Preference
> Prefer immutable data structures.

- **Detection:** Mutable global/static state; functions that mutate their arguments (unless the mutation is the stated purpose).
- **Threshold:** Any mutable shared state that is not explicitly synchronized.

### 5.2 Pure Functions Where Possible
> Functions without side effects are easier to test and reason about.

- **Detection:** Functions that read/write files, network, DB, global state, or random without clear documentation.
- **Threshold:** Any impure function masquerading as pure (no indication in name or docs).

### 5.3 No Hidden Side Effects
> Side effects must be obvious from the function signature/name.

- **Detection:** Function that performs I/O, mutates global state, or throws but has no indication in its name, type signature, or documentation.
- **Threshold:** Any hidden side effect.

### 5.4 No Shared Mutable State Without Synchronization
> Shared mutable state must be protected.

- **Detection:** Global/static variables, captured mutable variables in closures/callbacks, shared references across threads/goroutines without mutex/atomic/channel.
- **Threshold:** Any unsynchronized shared mutable state.

---

## 6. Error Handling

### 6.1 Don't Swallow Errors
> Errors must be handled or propagated, not silently ignored.

- **Detection:** Empty catch blocks; `// ignore error` comments; ignored return values from error-returning functions; `void`-cast of error-returning expression.
- **Threshold:** Any swallowed error.

### 6.2 Don't Lose Error Context
> Errors should carry enough context to diagnose and fix.

- **Detection:** Generic error types (`Box<dyn Error>`, `Exception`, `string` errors) without wrapping; re-throwing caught exceptions without adding context; logging the error message but not the values that caused it.
- **Threshold:** Any error that loses the root cause or context.

### 6.3 Handle All Branches
> Every conditional branch, match arm, or switch case must be explicitly handled.

- **Detection:** Default/else branch that is empty, logs "unexpected" and continues, or panics without explanation; incomplete pattern matches (in languages that allow it).
- **Threshold:** Any unhandled branch in a match/switch/if-else chain.

### 6.4 Structured Error Types
> Use custom error types rather than generic errors.

- **Detection:** Functions returning `Result<_, String>`, `Either<_, Exception>`, or similar generic error types in public APIs.
- **Threshold:** Public API returning generic error types.

---

## 7. Architecture

### 7.1 Dependency Rule (Layered Architecture)
> Source code dependencies must point inward — outer layers depend on inner layers, never inward on outward.

- **Detection:** UI/transport layer directly importing database driver; business logic importing HTTP library; persistence layer importing view/UI types.
- **Threshold:** Any inward-to-outward dependency.

### 7.2 Business Logic Independence
> Business logic should be independent of frameworks, databases, and UI.

- **Detection:** Business logic files importing framework-specific types; SQL embedded in business logic; UI rendering logic mixed with data processing.
- **Threshold:** Any such mixing.

### 7.3 Explicit Dependencies Over Implicit/Global
> Dependencies should be explicitly passed or declared, not obtained from global state.

- **Detection:** Singleton access pattern, static/service locator, global variable, ambient context, thread-local storage for dependencies.
- **Threshold:** Any use of global state for dependency resolution.

### 7.4 Composition Over Inheritance
> Prefer composing small units of behavior over deep inheritance hierarchies.

- **Detection:** Inheritance chain >2 levels deep (excluding language-level base classes); subclass that overrides most methods of the parent.
- **Threshold:** >2 levels of inheritance; subclass overriding >50% of parent methods.

### 7.5 Open for Extension, Closed for Modification (OCP)
> Modules should be open for extension but closed for modification.

- **Detection:** Adding a new feature requires modifying existing code rather than adding new code; flag/switch-based behavior branching instead of polymorphism/strategy.
- **Threshold:** Feature additions consistently modify existing files instead of adding new ones.

---

## 8. Testing

### 8.1 Test Behavior, Not Implementation
> Tests should verify observable behavior, not internal implementation details.

- **Detection:** Tests that assert which methods were called (verify/mock assertions) rather than the outcome; tests that access private members; tests that break on refactoring that does not change behavior.
- **Threshold:** >2 implementation-asserting tests per test file.

### 8.2 Arrange-Act-Assert (AAA) Pattern
> Tests should be organized into clear phases.

- **Detection:** Tests with interleaved setup and assertion; tests with no clear act step; tests that assert before the act.
- **Threshold:** Flag tests where a reader cannot easily identify the three phases.

### 8.3 One Logical Assertion Per Test
> Each test should verify one behavior.

- **Detection:** Tests with multiple unrelated assertions that test different behaviors; tests that assert across multiple independent scenarios.
- **Threshold:** >3 assertions about different outcomes in one test.

### 8.4 Don't Mock What You Don't Own
> Mock external boundaries, not third-party library internals.

- **Detection:** Mocks for standard library types; mocks for framework internals; mocks for types from third-party libraries (unless the library is the abstraction boundary).
- **Threshold:** Any mock of a type not owned by the project.

### 8.5 Test One Failure Mode at a Time
> Each test should verify one specific failure scenario.

- **Detection:** Tests that combine multiple failure conditions; tests that verify a success case but label themselves as error tests.
- **Threshold:** Any test testing multiple failure modes.

---

## 9. Configuration & Environment

### 9.1 Configuration Over Hardcoding
> Values that change between deployments should be configuration, not code.

- **Detection:** Hardcoded URLs, ports, timeouts, feature flags, credentials in source code.
- **Threshold:** Any deployment-varying value hardcoded.

### 9.2 Fail on Missing Configuration
> Required configuration should cause a startup failure, not a runtime error.

- **Detection:** Fallback defaults that silently activate in production; `||` operator with dev defaults; optional parsing that returns null for required config.
- **Threshold:** Any required config with a silent default.

### 9.3 Environment Separation
> Development and production environments should differ only in configuration values, not code paths.

- **Detection:** `if (isDev) { ... }` or similar environment-detection branching in business logic; development-only code paths mixed with production logic.
- **Threshold:** Any environment check in production code.

---

## 10. Concurrency & Resource Management

### 10.1 No Blocking Calls in Async Context
> Blocking I/O in async code defeats the purpose of async.

- **Detection:** `std::thread::sleep()`, `time.sleep()`, synchronous I/O in async functions.
- **Threshold:** Any occurrence.

### 10.2 Unbounded Resources Must Not Grow Forever
> Collections, queues, caches, and buffers must have size limits.

- **Detection:** Unbounded `Vec`/`List`/channels used as accumulation buffers; caches without eviction policy; in-memory event/request logs that grow with each request.
- **Threshold:** Any collection that grows without bound under normal operation.

### 10.3 Cancel Safety
> Async operations must be safe to cancel.

- **Detection:** Operations that acquire a resource, await, then release; holding a mutex across an await point; partial writes on cancellation.
- **Threshold:** Any mutex held across await; any resource acquisition without cleanup on cancellation.

### 10.4 Timeout Every External Call
> Every call to an external system must have a timeout.

- **Detection:** HTTP clients without timeout; database queries without statement timeout; file operations on network filesystems without timeout.
- **Threshold:** Any external call without explicit timeout.

---

## How to Use This Rubric

1. **During audit:** Cross-reference code against these principles.
2. **For violations:** Map to the appropriate dimension (Maintainability, Security, Stability, etc.).
3. **Severity mapping:** Use the severity listed for each principle as the default, then adjust up or down based on context (how many places, how central, how likely to cause real failure).
4. **Evidence requirement:** For each violation, cite which principle is violated and why, with specific code evidence.
5. **Do not report every minor violation** — focus on violations that create real engineering risk.
6. **Example format:**

```
### Finding: SRP violation in UserService — 3 responsibilities in one class

- Severity: Medium
- Confidence: High
- Category: Maintainability
- Status: Confirmed
- Principle violated: Single Responsibility (1.1)
- Evidence:
  - File: src/services/user.rs:1-250
  - Relevant behavior: UserService handles DB queries, email sending, and permission checks.
- Why it matters: Each responsibility has different change reasons and different test requirements.
- ...
```
