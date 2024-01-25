#!/bin/bash

echo "Started udt postgis DB restore."
echo

OPTSTRING=":f:"

DB_CONTAINER_ID=`docker ps | grep udtpostgis | grep postgis/postgis | awk '{ print $1 }'`


while getopts ${OPTSTRING} opt; do
  case ${opt} in
    f)
        #filename="${OPTARG##*/}"
        #docker cp ${OPTARG} ${DB_CONTAINER_ID}:/
        cat ${OPTARG} | docker exec ${DB_CONTAINER_ID} psql -U udt -d udt
      ;;
  esac
done
