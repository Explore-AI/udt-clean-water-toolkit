#!/bin/bash

echo "Started udt Neo4j DB backup. Ensure you have a data/db_backups/ folder in the root directory of this project. If not we will make one."
echo

BASE_DIR=../../..
DB_BACKUPS_DIR=${BASE_DIR}/data/db_backups

if [ ! -d ${DB_BACKUPS_DIR} ]; then
    mkdir -p ${DB_BACKUPS_DIR}
fi

DB_CONTAINER_ID=`docker ps | grep udtneo4j | grep neo4j:latest | awk '{ print $1 }'`


if [[ -z ${DB_CONTAINER_ID} ]];then
  echo "${DB_CONTAINER_ID} is not running, please run it using the docker-compose-postgis.yml"
else
  docker stop ${DB_CONTAINER_ID}
  docker run -it  --rm --env-file ../../docker/env_files/.db_env --volume=docker_neo4j-data:/data --volume=docker_neo4j-backup:/backups neo4j/neo4j-admin neo4j-admin database dump neo4j --to-path=/backups
  docker start ${DB_CONTAINER_ID}
  docker cp ${DB_CONTAINER_ID}:/backups/neo4j.dump ${DB_BACKUPS_DIR}

fi