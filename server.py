import os
import json
from pathlib import Path
from typing import Any

DEFAULT_CONFIG_PATH = Path("~/.mcp-mariadb/config.yaml").expanduser()

try:
    import yaml
except ImportError:  # pragma: no cover - exercised when dependency missing
    yaml = None

try:
    import pymysql
    from pymysql.cursors import DictCursor
except ImportError:  # pragma: no cover - exercised when dependency missing
    pymysql = None
    DictCursor = None

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:  # pragma: no cover - exercised when dependency missing
    FastMCP = None


def load_config(config_path: str | None = None) -> dict[str, Any]:
    """Load MariaDB settings from the configured YAML file."""
    path = Path(config_path or os.getenv("MCP_MARIADB_CONFIG", str(DEFAULT_CONFIG_PATH))).expanduser()
    if not path.exists():
        return {"mariadb": {}}

    if yaml is None:
        raise RuntimeError("PyYAML is required to parse the config file")

    with path.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle) or {}

    if not isinstance(loaded, dict):
        raise ValueError("Config file must contain a top-level mapping")

    return loaded


def _get_connection(config: dict[str, Any]):
    if pymysql is None or DictCursor is None:
        raise RuntimeError("pymysql is required to connect to MariaDB")

    mariadb_config = config.get("mariadb", {})
    if not isinstance(mariadb_config, dict):
        raise ValueError("The mariadb section must be a mapping")

    required_fields = ["host", "database", "username", "password"]
    missing_fields = [field for field in required_fields if not mariadb_config.get(field)]
    if missing_fields:
        raise ValueError(f"Missing required MariaDB config values: {', '.join(missing_fields)}")

    port = mariadb_config.get("port", 3306)
    return pymysql.connect(
        host=mariadb_config["host"],
        port=int(port),
        user=mariadb_config["username"],
        password=mariadb_config["password"],
        database=mariadb_config["database"],
        cursorclass=DictCursor,
    )


def execute_sql(sql: str, config: dict[str, Any] | None = None) -> dict[str, Any]:
    """Execute a SQL statement and return the matching rows."""
    effective_config = config or load_config()
    connection = _get_connection(effective_config)

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall() or []
            rowcount = cursor.rowcount if cursor.rowcount is not None else len(rows)
        connection.commit()
        return {"rowcount": rowcount, "rows": rows}
    finally:
        connection.close()


if FastMCP is not None:
    mcp = FastMCP("mariadb")

    @mcp.tool()
    def executesql(sql: str) -> dict[str, Any]:
        return execute_sql(sql)
else:
    mcp = None


if __name__ == "__main__":
    if mcp is None:
        raise SystemExit("Install the mcp package to run the server")
    mcp.run(transport="stdio")
