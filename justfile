test:
    python -m pytest
run:
    MCP_MARIADB_CONFIG=example-config.yaml python server.py

start-mariadb:
    cd testing && docker compose up -d 

mysql:
    docker exec -it mcp-mariadb-test mariadb -u app -psecret app
