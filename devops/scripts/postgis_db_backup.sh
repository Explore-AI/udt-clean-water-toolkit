#!/bin/bash

echo "Started udt postgis DB backup. Ensure you have a data/db_backups/ folder in the root directory of this project. If not we will make one."
echo

BASE_DIR=../..
DB_BACKUPS_DIR=${BASE_DIR}/data/db_backups

if [ ! -d ${DB_BACKUPS_DIR} ]; then
    mkdir -p ${DB_BACKUPS_DIR}
fi

DB_CONTAINER_ID=`docker ps | grep udtpostgis | grep postgis/postgis | awk '{ print $1 }'`

CURRENT_DATETIME=`date "+%m-%d-%Y_%H-%M-%S"`
BACKUP_FILE_NAME=${DB_BACKUPS_DIR}/udt_postgis_db_backup_${CURRENT_DATETIME}.sql

docker exec -it ${DB_CONTAINER_ID} pg_dump -U udt -Fc udt > ${BACKUP_FILE_NAME}
