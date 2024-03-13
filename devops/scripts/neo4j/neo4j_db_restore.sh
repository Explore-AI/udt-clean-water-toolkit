#!/bin/bash

echo "Started udt Neo4j DB backup. Ensure you have a data/db_backups/ folder in the root directory of this project. If not we will make one."
echo

BASE_DIR=../../..
DB_BACKUPS_DIR=${BASE_DIR}/data/db_backups

if [ ! -d ${DB_BACKUPS_DIR} ]; then
    mkdir -p ${DB_BACKUPS_DIR}
fi


# Start the backup container
docker run -it --rm --env-file ../../docker/env_files/.db_env --volume=docker_neo4j-data-upgrade:/data --volume=docker_neo4j-backup:/backups neo4j/neo4j-admin neo4j-admin database load neo4j --from-path=/backups


echo "A new database dump has been initiated, please use the following logic"
echo "Comment out the following - neo4j-backup:/backups and uncomment #- neo4j-data-upgrade:/data in docker-compose-postgis.yml and run it again"

