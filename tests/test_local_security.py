import unittest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.core.local_security import LocalSecurityMiddleware


class LocalSecurityTests(unittest.TestCase):
    def setUp(self):
        app = FastAPI()
        app.add_middleware(LocalSecurityMiddleware)
        @app.get("/")
        def home():
            return {"ok": True}
        @app.post("/api/admin/login")
        def login():
            return {"ok": True}
        @app.post("/api/tokens")
        def add_token():
            raise AssertionError("Account handler must not run")
        self.client = TestClient(app)

    def test_public_host_rejected(self):
        self.assertEqual(self.client.get("/", headers={"host": "attacker.example"}).status_code, 403)

    def test_cross_origin_login_rejected(self):
        response = self.client.post("/api/admin/login", headers={"origin": "https://attacker.example"})
        self.assertEqual(response.status_code, 403)

    def test_account_import_blocked_in_preview(self):
        self.assertEqual(self.client.post("/api/tokens").status_code, 403)

    def test_local_login_allowed_and_security_headers(self):
        response = self.client.post("/api/admin/login", headers={"origin": "http://testserver"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["x-frame-options"], "DENY")


if __name__ == "__main__":
    unittest.main()
