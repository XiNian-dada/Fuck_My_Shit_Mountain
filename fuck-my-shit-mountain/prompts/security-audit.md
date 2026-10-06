# Security Audit Prompt

Use the fuck-my-shit-mountain skill in **security mode**.

Shared setup, coverage, report template, HTML, and lint rules live in `references/report-format.md`; load that reference before producing the report.

Focus only on security-relevant risks.

## Audit Areas (see principle 4.6: Least Privilege)

### Authentication & Authorization
- How does the application identify users?
- How does it determine what each user can do?
- Can a user access resources they should not have access to?
- Are there hardcoded credentials, tokens, or API keys?
- How are sessions managed? Token lifecycle?

### Input & Output
- Injection vectors (command, SQL, NoSQL, LDAP, template)
- Path traversal in file operations
- SSRF in URL fetching or proxy features
- CORS configuration
- CSRF protection
- Serialization of untrusted data

### Secrets & Configuration
- Hardcoded secrets in code, tests, or config files
- Secrets in environment variables with unsafe defaults
- Secrets in logs, error messages, or debug output
- Config files committed to version control
- Unsafe default configurations

### Network & Transport
- TLS configuration
- WebSocket authentication and origin checking
- API endpoint exposure (internal vs external)
- Rate limiting and brute-force protection

### Dependencies
- Known vulnerable dependencies
- Supply chain risks (install scripts, postinstall hooks, build-time code execution)
- Unnecessary dependencies expanding attack surface
- Dependency confusion (public package shadowing internal name)

### Operational Security
- File permissions on sensitive files
- Logging of sensitive data (passwords, tokens, PII)
- Debug endpoints left enabled
- Error handling that leaks internal state
- Information disclosure in response headers or error pages

## Rules

1. Every security finding must include an attack precondition and attack path.
2. Do not report theoretical vulnerabilities without a realistic exploitation path.
3. Separate confirmed issues from suspected issues.
4. For each issue, include a specific mitigation and a regression test.

## Finding Format

Use the common fields in `templates/issue-card.md` and the format rules in `references/report-format.md`. Specialized evidence supplements those fields; it does not replace them.

Include these additional details when they help substantiate a finding:

- Attack precondition:
- Attack path:
- Impact:
- Mitigation:

## Focus

Do not waste output on:
- HTTPS enforcement when the app is designed for local-only use
- CSP headers when the app has no browser UI
- Theoretical supply chain attacks without evidence
- Missing auth on endpoints that are explicitly public
