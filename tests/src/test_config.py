import os
import unittest

from core.config import Settings, get_settings


class TestSettings(unittest.TestCase):
    def test_defaults(self) -> None:
        settings = Settings()
        self.assertEqual(settings.MCP_HOST, "127.0.0.1")
        self.assertEqual(settings.MCP_PORT, 3000)
        self.assertTrue(settings.server_url.endswith(":3000/mcp"))
        self.assertIn("realms/openspace", str(settings.OAUTH_ISSUER_URL))

    def test_env_overrides(self) -> None:
        os.environ["MCP_HOST"] = "0.0.0.0"
        os.environ["MCP_PORT"] = "4000"
        os.environ["MCP_PATH"] = "/custom"

        settings = Settings()
        self.assertEqual(settings.MCP_HOST, "0.0.0.0")
        self.assertEqual(settings.MCP_PORT, 4000)
        self.assertEqual(settings.server_url, "http://0.0.0.0:4000/custom")

        # clean up
        del os.environ["MCP_HOST"]
        del os.environ["MCP_PORT"]
        del os.environ["MCP_PATH"]

    def test_cached_get_settings(self) -> None:
        s1 = get_settings()
        s2 = get_settings()
        self.assertIs(s1, s2)


if __name__ == "__main__":
    unittest.main()
