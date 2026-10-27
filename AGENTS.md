# Development handoff

Read PROJECT_CONTEXT.md before changing this fork. Preserve the upstream MIT license and attribution.

Never commit Google cookies, access tokens, passwords, account lists, browser profiles, databases, generated media, or local configuration. Use placeholders in examples and tests. Do not print credentials in logs.

Do not spend account credits or submit live generation requests as part of tests unless the user authorizes that test. Use mocks for routine verification. Stop for user interaction when Google requires login or verification; do not introduce CAPTCHA bypass or anti-detection features.

Before a change, inspect the relevant code and tests. Run focused tests appropriate to that change and report what was actually verified. Do not claim that this application is ban-proof or that all upstream features work without testing them.

Keep changes small and document setup or behavior changes. Commit source changes so another developer or AI can continue from the repository.
