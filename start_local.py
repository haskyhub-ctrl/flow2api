"""Create private local settings, then run the reviewed web preview on loopback."""
import os
import secrets
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def prepare():
    os.chdir(ROOT)
    settings = ROOT / "config" / "setting.toml"
    if not settings.exists():
        content = (ROOT / "config" / "setting_example.toml").read_text(encoding="utf-8")
        password = secrets.token_urlsafe(24)
        content = content.replace('api_key = "han1234"', f'api_key = "{secrets.token_urlsafe(32)}"')
        content = content.replace('admin_password = "admin"', f'admin_password = "{password}"')
        content = content.replace('host = "0.0.0.0"', 'host = "127.0.0.1"')
        content = content.replace('port = 8000', 'port = 38000')
        content = content.replace('captcha_method = "yescaptcha"', 'captcha_method = "disabled"')
        settings.write_text(content, encoding="utf-8")
        (ROOT / "LOCAL_ACCESS.txt").write_text(
            f"URL: http://127.0.0.1:38000\nUsername: admin\nPassword: {password}\n"
            "Local preview only. Account import and generation are disabled pending review.\n",
            encoding="utf-8",
        )
    os.environ.setdefault("FLOW2API_REVIEW_MODE", "1")


if __name__ == "__main__":
    prepare()
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=38000, log_level="info")
