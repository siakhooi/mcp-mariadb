# mcp-mariadb

A simple Model Context Protocol (MCP) server for MariaDB written in Python.

## Features

- Loads MariaDB connection settings from a YAML config file
- Uses the environment variable MCP_MARIADB_CONFIG when set
- Defaults to ~/.mcp-mariadb/config.yaml when the environment variable is not set
- Exposes one tool: executesql

## Installation

```bash
cd /workspaces/mcp-mariadb
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Create a YAML file such as:

```yaml
mariadb:
  host: localhost
  database: app
  username: app
  password: secret
```

Set the environment variable to point at it:

```bash
export MCP_MARIADB_CONFIG=/path/to/config.yaml
```

If the environment variable is not set, the server will look for:

```bash
~/.mcp-mariadb/config.yaml
```

## Running the server

```bash
python server.py
```

## Tool usage

The server exposes a tool named executesql. It accepts a SQL string and returns the rows and row count from the MariaDB query.

Example:

```json
{
  "sql": "SELECT * FROM users LIMIT 10"
}
```

## Badges
[![Wise](https://img.shields.io/badge/Funding-Wise-33cb56.svg?logo=wise)](https://wise.com/pay/me/siakn3)
![visitors](https://hit-tztugwlsja-uc.a.run.app/?outputtype=badge&counter=ghmd-mcp-mariadb)
