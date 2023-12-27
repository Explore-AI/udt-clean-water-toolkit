#!/bin/bash

echo "Started udt DB reset. The udt database will be dropped and recreated. "

DB_CONTAINER_ID=`docker ps | grep udtpostgis | grep postgis/postgis | awk '{ print $1 }'`

#docker exec -it ${DB_CONTAINER_ID} psql --user udt -c "select pg_terminate_backend(pid) from pg_stat_activity where datname='udt_api2';"

#CREATE USER udt with password '[somepassword]' superuser;
docker exec -it ${DB_CONTAINER_ID} psql --user udt -c "drop database udt"
docker exec -it ${DB_CONTAINER_ID} psql --user udt -c "create database udt"

echo "DB reset complete."

# docker exec -it {DB_CONTAINER_ID} psql
