# Confidence Rubric

## High

- The finding is directly observed in the code.
- The evidence includes a specific code path, function, or configuration.
- The failure scenario can be reproduced or clearly traced.
- The issue is confirmed by a test failure or runtime behavior.
- No ambiguity in interpretation — the code does what the finding describes.

### When to use

- You have read the relevant code and can point to exact lines.
- You have traced a control flow and identified a bug.
- You have tested the behavior and confirmed the issue.
- A comment points to a risk that you independently verified in the code or runtime behavior; the comment alone is insufficient.

## Medium

- The finding is inferred from code patterns, not directly observed.
- The evidence points to a code area but the exact trigger is unclear.
- The issue depends on external factors (OS, network, load).
- The code follows a pattern that is commonly dangerous.
- You have moderate confidence that the issue is real but lack reproduction.

### When to use

- The pattern matches known anti-patterns but you have not tested it.
- Error handling is missing but you cannot confirm it causes real failures.
- A dependency has known vulnerabilities but the usage surface is small.
- The logic is hard to follow and likely incorrect, but not proven.

## Low

- The finding is speculative.
- The evidence is weak or indirect.
- The issue depends on unlikely conditions or configurations.
- You are inferring risk from naming or structure without reading the full flow.
- The code looks unusual but may be intentional.

### When to use

- You have not fully read the relevant code.
- The finding is based on file size, structure, or naming only.
- The risk depends on future scale or usage patterns.
- You want to flag an area for human review.

## Guidelines

- If you are not sure, use **Medium** or **Low**, not **High**.
- Be conservative. It is better to under-state confidence than over-state it.
- If the confidence is Low, consider whether the finding is worth reporting at all. Low-confidence issues should be rare.
- A finding can have different confidence levels for different aspects. State the confidence for the core claim.
