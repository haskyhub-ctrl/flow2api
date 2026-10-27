# Flow video account manager

## Goal

The owner has approximately 20 Google AI Pro accounts and wants a single interface for queued video generation without manually switching accounts. Each account retains its own credits and service limits. The user requested a public GitHub repository to continue development across machines and AI assistants.

## Starting point

- Upstream: https://github.com/TheSmallHanCat/flow2api
- Imported commit: 1bcb9275d154c330d29cac3ba836a13393ff49c7
- License: MIT; preserve LICENSE and upstream attribution.
- Imported on: 2026-10-27.
- Source cloned and license inspected. No dependencies installed, server started, account credentials entered, or live video generations tested during the import.
- Upstream documents token pooling, concurrency controls, a management interface, credit queries, and video generation. These are upstream claims, not verified end-to-end results.

## Constraints

Google AI Pro subscription credits are separate from Gemini API billing. This application uses an unofficial Flow integration. Reliability, account restrictions, and credential handling need review before connecting real accounts. No guarantee against account suspension is possible.

## Suggested next work

1. Review outgoing network calls, embedded service credentials, CAPTCHA-provider integrations, authentication, and logging before running with real accounts.
2. Prefer locally retained sessions and explicit user verification; remove unwanted third-party integrations.
3. Add a durable prompt queue with progress, per-account credit budgets, pause/resume, and bounded retries. Respect service errors and limits.
4. Add a Vietnamese interface and a clear local setup guide.
5. Validate with mocks first, then a user-authorized small live test.

## Code orientation

- main.py: application entry point.
- src/api/: HTTP endpoints.
- src/core/: shared configuration and core functionality.
- src/services/: Flow integration and account/session services.
- static/: web interface.
- extension/: browser extension code.
- tests/: upstream tests.
- config/setting_example.toml: example local configuration.

See the upstream README.md for existing setup instructions. Review those instructions and external integrations before following them.
