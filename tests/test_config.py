import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import server


class ConfigLoadingTests(unittest.TestCase):
    def test_reads_config_from_environment_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config_path.write_text(
                "mariadb:\n  host: localhost\n  database: app\n  username: user\n  password: secret\n",
                encoding="utf-8",
            )

            with patch.dict(os.environ, {"MCP_MARIADB_CONFIG": str(config_path)}, clear=False):
                config = server.load_config()

            self.assertEqual(config["mariadb"]["host"], "localhost")
            self.assertEqual(config["mariadb"]["database"], "app")
            self.assertEqual(config["mariadb"]["username"], "user")
            self.assertEqual(config["mariadb"]["password"], "secret")

    def test_uses_default_config_path_when_environment_is_missing(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(server, "DEFAULT_CONFIG_PATH", Path("/tmp/test-home/.mcp-mariadb/config.yaml")):
                config = server.load_config()

        self.assertIsNotNone(config)


if __name__ == "__main__":
    unittest.main()
