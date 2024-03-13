#!/bin/bash

echo "Started udt Neo4j DB backup. Ensure you have a data/db_backups/ folder in the root directory of this project. If not we will make one."
echo

BASE_DIR=../../..
DB_BACKUPS_DIR=${BASE_DIR}/data/db_backups

if [ ! -d ${DB_BACKUPS_DIR} ]; then
    mkdir -p ${DB_BACKUPS_DIR}
fi

DB_CONTAINER_ID=`docker ps | grep udtneo4j | grep neo4j:latest | awk '{ print $1 }'`
DB_BACKUP_CONTAINER_ID=`docker ps | grep udtneo4j-backup | grep neo4j/neo4j-admin | awk '{ print $1 }'`

CURRENT_DATETIME=`date "+%d-%m-%Y_%H-%M-%S"`
BACKUP_FILE_NAME=udt_neo4j_db_backup_${CURRENT_DATETIME}.dump


docker stop ${DB_CONTAINER_ID}

docker exec -it ${DB_BACKUP_CONTAINER_ID} neo4j-admin database dump neo4j --to-path=/backups

docker cp ${DB_BACKUP_CONTAINER_ID}:/backups/neo4j.dump ${DB_BACKUPS_DIR}

mv ${DB_BACKUPS_DIR}/neo4j.dump ${DB_BACKUPS_DIR}/${BACKUP_FILE_NAME}

docker start ${DB_CONTAINER_ID}

