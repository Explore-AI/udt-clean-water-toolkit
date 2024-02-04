# Instructions

To set up an instance of the service do the following:

1) Navigate to the folder `docker/env_files`
2) Make changes to the env file by running:
    ```bash
    cp .db_env.example .db_env
    ```
3) Adjust the values in `.db_env`. If you happen to change 
the variable `POSTGRES_PASS` make sure you also adjust it in
the `docker-compose-cwa-geodjango-dev.yml` in the healthcheck
section to match the value in your env file.
4) Run the setup script. If you are using a newer version of 
`docker compose` you can run it as:
    ```bash
    ./dev_setup.sh
    ```
    If you are running the older version you can run:
    ```bash
    ./dev_setup.sh docker-compose
    ```
