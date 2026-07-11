test:
    python -m pytest
run:
    MCP_MARIADB_CONFIG=example-config.yaml python server.py
build:
    ./scripts/build.sh
release:
    ./scripts/release.sh

start-mariadb:
    cd testing && docker compose up -d
stop-mariadb:
    cd testing && docker compose down
create-network:
    docker network create mcp-net
mysql:
    docker exec -it mcp-mariadb-test mariadb -u app -psecret app
