#!/bin/bash

echo "Setting up the cwa_geodorm app for development."
echo "The following actions will take place:"
echo "udt postgis server will be setup."
echo "A udt postgis database will be created."
echo "A udt superuser will be created on the postgis database."
echo "pip packages will be installed for the cwa_geodorm app."
echo "pip packages will be installed for the cwm in dev mode."

docker-compose -f ../docker/docker-compose-postgis.yml -f ../docker/docker-compose-cwa-geodorm-dev.yml up -d

CWA_GEODORM_CONTAINER_ID=`docker ps | grep udtcwageodormdev | grep cwa_geodorm_dev | awk '{ print $1 }'`

docker exec -it ${CWA_GEODORM_CONTAINER_ID} pip install -r requirements.txt -r dev-requirements.txt

# TODO: call db init script directly instead.
# For some reason ./postgis_db_init.sh didn't work.
# May be a timing issue.

./postgis_db_init.sh

# source ../docker/env/.db_env

# DB_CONTAINER_ID=`docker ps | grep udtpostgis | grep postgis/postgis | awk '{ print $1 }'`

# docker exec -it ${DB_CONTAINER_ID} psql --user postgres -c "create database udt"
# docker exec -it ${DB_CONTAINER_ID} psql --user postgres -c "create user udt with superuser password '${POSTGRES_PASSWORD}'"


docker exec -it ${CWA_GEODORM_CONTAINER_ID} python3 main.py migrate

echo "cwa_geodeom app dev setup complete."
