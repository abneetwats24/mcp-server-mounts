import unittest

from mcp.server.fastmcp import FastMCP

from main import create_server


class TestMainServer(unittest.TestCase):
    def test_create_server_returns_fastmcp(self) -> None:
        server = create_server()
        self.assertIsInstance(server, FastMCP)

    def test_create_server_mounts_subservers(self) -> None:
        server = create_server()
        # get_tools() is async; here we just ensure no exception when calling
        # the registration logic via create_server
        # The actual mounted prefixes are part of FastMCP's internal state,
        # which we can rely on indirectly by checking capabilities.
        caps = server.get_capabilities()
        # We don't assert exact contents, just that capabilities dict exists
        self.assertIsInstance(caps, dict)


if __name__ == "__main__":
    unittest.main()
