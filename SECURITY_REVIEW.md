# Targeted security review — 2026-10-27

## Conclusion

Do not connect Google accounts to the original build without review. A concrete credential-disclosure path was found: when `flow2api_team` is selected, upstream collects Google request cookies and puts them in `task.cookie` in a request to the hardcoded `captcha.haqimi.uk` service. The upstream tests explicitly include SID and OSID in this payload. This establishes transmission behavior, not the author's intent or proof that the service steals accounts. It is not enabled by the original example's default `yescaptcha` setting.

This fork removes that cookie payload, disables both team-service entry points, clears its embedded endpoint/key, and prevents the helper from collecting cookies. Regression tests assert that these paths fail before network access or cookie reads.

No real Google credentials were entered and no live generation was run during this review.

## Other findings and changes

| Finding | Change in this fork |
| --- | --- |
| Five request locations disabled TLS certificate verification, including downloads and proxy/browser paths | Re-enabled certificate verification at those locations |
| Default admin/admin password and a public-interface example bind | Launcher generates a random private password/API key; binds to 127.0.0.1:38000; startup rejects unchanged default admin password |
| Debug logger could expose Google cookies, short tokens, structured response credentials and proxy URLs | Redact sensitive headers, credential fields and query keys; omit unstructured bodies; debug remains disabled |
| Browser modules could install packages/browsers implicitly, with alternate mirrors | Installer functions now refuse; browser installation no longer runs on module import |
| Login/admin pages loaded executable Tailwind code from an external CDN | Replaced with compiled local CSS; versioned build dependencies recorded in package.json and pnpm-lock.yaml |
| Wildcard CORS and no explicit local-host/cross-origin-write gate | Removed wildcard CORS; added local-host validation and cross-origin write rejection |
| Known dependency advisories for the initially installed curl-cffi, python-multipart, Starlette and pip | Updated affected runtime packages and local pip; upgraded FastAPI to support the patched Starlette; follow-up pip-audit reported no known advisories |

## Preview boundary

The default `FLOW2API_REVIEW_MODE=1` is an intentionally restricted local preview. Login and dashboard reads work. Account import, configuration writes, tests that call Google, and generation requests are blocked by HTTP middleware. Startup refuses an existing account database, does not start the credential refresher, and disables CAPTCHA/browser startup. Use a clean installation for preview.

The launcher stores a generated admin password and API key in ignored local files. They are not encrypted against another process/user with filesystem access. Do not share LOCAL_ACCESS.txt, config/setting.toml, data/, logs, browser profiles, or environment files.

## Remaining work before connecting accounts or hosting

- Review every remaining configurable outbound URL, redirects, media downloads and remote-browser integration for credential disclosure and SSRF.
- Replace raw Google-cookie import with a deliberately designed local session workflow. The upstream database stores account credentials in plaintext.
- Add session expiration, login throttling and secure deployment authentication. Current admin sessions have no explicit expiration.
- Review browser cleanup/process termination and embedded browser automation separately before enabling them. Those paths were not exercised in preview.
- Do not treat `FLOW2API_REVIEW_MODE=0` as security approval. It merely removes the preview gate; this review does not approve Internet deployment or live multi-account use.
- No anti-ban guarantee is possible. Any future account workflow must respect Google verification and service limits.

## Verification and limits

40 focused tests passed, with 8 additional unittest subtests reported. Coverage includes removal of the team service, cookie/token redaction, host and origin checks, preview write blocking, existing localization, mocked token import, and cookie snapshots. Eleven HTTP smoke assertions passed against the running local app, including login, dashboard, local CSS, empty accounts and blocked generation/import.

Dependency scan: pip-audit reported no known vulnerabilities in the updated local Python environment at review time. This is a database lookup, not a malware analysis of every dependency. JavaScript build packages were not covered by pip-audit.

This was a targeted source review of network destinations, credential flows, process execution, authentication, logging, runtime installation, and startup. It was not an exhaustive line-by-line audit, independent penetration test, antivirus certification, or a live Google integration test. Not finding additional malware indicators is not proof of safety.

Upstream baseline: TheSmallHanCat/flow2api at 1bcb9275d154c330d29cac3ba836a13393ff49c7. Preserve its MIT license and attribution.
