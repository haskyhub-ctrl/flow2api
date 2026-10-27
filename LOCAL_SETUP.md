# Run the local web preview

Read SECURITY_REVIEW.md first. This fork is currently a local interface preview, not a completed live video generator.

On Windows, with Python 3.12 installed:

```powershell
git clone https://github.com/haskyhub-ctrl/flow2api.git
cd flow2api
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe start_local.py
```

Open http://127.0.0.1:38000. The launcher creates LOCAL_ACCESS.txt with the username and a random password. That file and the private config are ignored by Git. Keep the server process running while using the page; Ctrl+C stops a foreground launch. No browser extension is required for preview.

Default preview mode blocks Google account import, external account operations and video generation. No Google account, API key or credits are needed to inspect the interface. Do not follow the upstream README's account/CAPTCHA setup instructions yet.

The compiled stylesheet is committed, so Node.js is not needed to run the preview. To rebuild styles after changing HTML, install the locked JavaScript dev dependencies with pnpm, then run `pnpm run build:css`.

For another AI or developer: read AGENTS.md, PROJECT_CONTEXT.md and SECURITY_REVIEW.md before changing the application.
