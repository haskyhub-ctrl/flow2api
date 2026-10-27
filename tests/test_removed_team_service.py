"""The fork must never forward Google cookies to the upstream team service."""
import unittest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException
from src.core.config import FLOW2API_TEAM_CAPTCHA_BASE_URL, FLOW2API_TEAM_CAPTCHA_CLIENT_KEY
from src.services.flow_client import FlowClient


class RemovedTeamServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_no_embedded_destination_or_key(self):
        self.assertEqual(FLOW2API_TEAM_CAPTCHA_BASE_URL, "")
        self.assertEqual(FLOW2API_TEAM_CAPTCHA_CLIENT_KEY, "")

    async def test_request_blocked_before_any_network(self):
        client = FlowClient.__new__(FlowClient)
        with patch("src.services.flow_client.AsyncSession") as network:
            with self.assertRaisesRegex(RuntimeError, "disabled"):
                await client._get_api_captcha_token("flow2api_team", "example")
            network.assert_not_called()

    async def test_google_cookies_never_collected_for_team_service(self):
        client = FlowClient.__new__(FlowClient)
        client._resolve_flow_frontend_cookie_storage = AsyncMock()
        with self.assertRaisesRegex(RuntimeError, "disabled"):
            await client._build_team_captcha_cookie_map(1)
        client._resolve_flow_frontend_cookie_storage.assert_not_called()

    async def test_admin_helper_blocked_before_any_network(self):
        from src.api.admin import _solve_recaptcha_with_api_service
        with patch("src.api.admin.AsyncSession") as network:
            with self.assertRaises(HTTPException):
                await _solve_recaptcha_with_api_service("flow2api_team", "https://example.com", "example", "test")
            network.assert_not_called()
