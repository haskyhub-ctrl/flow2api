import logging
import unittest
from src.core.logger import DebugLogger, SecretFilter


class SecretRedactionTests(unittest.TestCase):
    def test_cookie_header_is_completely_removed(self):
        record=logging.LogRecord("test",20,"",1,"  cookie: SID=secret-cookie; OSID=other-secret",(),None)
        SecretFilter().filter(record)
        self.assertNotIn("secret-cookie",record.getMessage())
        self.assertNotIn("other-secret",record.getMessage())

    def test_nested_credential_collections_are_removed(self):
        logger=DebugLogger.__new__(DebugLogger)
        value=logger._truncate_large_fields({"ok":True,"session_cookies":[{"name":"SID","value":"secret"}],"nested":{"accessToken":"secret"}})
        self.assertTrue(value['ok'])
        self.assertEqual(value['session_cookies'],'[REDACTED]')
        self.assertEqual(value['nested']['accessToken'],'[REDACTED]')

    def test_short_token_is_not_exposed(self):
        self.assertEqual(DebugLogger.__new__(DebugLogger)._mask_token('short'),'[REDACTED]')
