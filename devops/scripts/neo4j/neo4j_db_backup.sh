#!/bin/bash

echo "Started udt postgis DB backup. Ensure you have a data/db_backups/ folder in the root directory of this project. If not we will make one."
echo

BASE_DIR=../../..
DB_BACKUPS_DIR=${BASE_DIR}/data/db_backups

if [ ! -d ${DB_BACKUPS_DIR} ]; then
    mkdir -p ${DB_BACKUPS_DIR}
fi

DB_CONTAINER_ID=`docker ps | grep udtneo4j | grep neo4j:latest | awk '{ print $1 }'`

CURRENT_DATETIME=`date "+%d-%m-%Y_%H-%M-%S"`
BACKUP_FILE_NAME=udt_neo4j_db_backup_${CURRENT_DATETIME}.sql

docker exec --name dump --entrypoint="/bin/bash" -it -v ${DB_BACKUPS_DIR}:/data ${DB_CONTAINER_ID} -c "neo4j-admin dump neo4j --to=/data/${BACKUP_FILE_NAME}"
