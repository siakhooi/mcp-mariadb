# mcp-mariadb

A simple Model Context Protocol (MCP) server for MariaDB.

## Features

- Loads MariaDB connection settings from a YAML config file
- Uses the environment variable MCP_MARIADB_CONFIG when set
- Defaults to ~/.mcp-mariadb/config.yaml when the environment variable is not set
- Exposes one tool: executesql

## Usages

### Installation

Use one of the sample in editor's mcp config file, put in your repo:
- `.cursor/mcp.json`
- `.antigravity/mcp.config.json`
- `.vscode/mcp.json`
- `.windsurf/mcp.config.json`

Notes: remove the `--network mcp-net` in the config file if your database is not configured to use the docker network `mcp-net`.

### Configuration

Create a YAML file such as:

```yaml
mariadb:
  host: localhost
  database: app
  username: app
  password: secret
```

## Tool usage

Ask the AI agent to use it when work with mariadb database.

## Badges
[![Wise](https://img.shields.io/badge/Funding-Wise-33cb56.svg?logo=wise)](https://wise.com/pay/me/siakn3)
![visitors](https://hit-tztugwlsja-uc.a.run.app/?outputtype=badge&counter=ghmd-mcp-mariadb)
