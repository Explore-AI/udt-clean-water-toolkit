Docker environment variables are placed in this directory.

1. Create env file for the database and neo4j and call it `.db_env`
    ```bash
    POSTGRES_PASSWORD=
    POSTGRES_USER=
    POSTGRES_DB=
    NEO4J_USER__ENV_VAR=
    NEO4J_PASSWORD__ENV_VAR=
    NEO4J_HOST__ENV_VAR=
    NEO4J_AUTH=
    NEO4J_server_config_strict__validation_enabled=false
    ```
2. Create env file for the GeoServer and call it `.geoserver_env`
    ```bash
    GEOSERVER_ADMIN_PASSWORD=
    INITIAL_MEMORY=2G
    MAXIMUM_MEMORY=4G
    STABLE_EXTENSIONS=
    COMMUNITY_EXTENSIONS=
    DB_BACKEND=POSTGRES
    HOST=udtpostgis
    POSTGRES_PORT=5432
    POSTGRES_DB=
    POSTGRES_USER=
    POSTGRES_PASS=
    SSL_MODE=allow
    POSTGRES_SCHEMA=public
    DISK_QUOTA_SIZE=5
    ```
   **Note:** The env variables `POSTGRES_DB,POSTGRES_USER,POSTGRES_PASS` should match those specified in the `.db_env`

3. You will need to also add django env variables.

