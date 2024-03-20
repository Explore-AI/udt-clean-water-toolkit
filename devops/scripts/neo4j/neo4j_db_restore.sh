#!/bin/bash

echo "Started udt neo4j DB restore."
echo

OPTSTRING=":f:"

DB_CONTAINER_ID=`docker ps | grep udtneo4j | grep neo4j:latest | awk '{ print $1 }'`


while getopts ${OPTSTRING} opt; do
    case ${opt} in
        f)
            if [[ -z ${DB_CONTAINER_ID} ]];then
                echo "${DB_CONTAINER_ID} is not running, please run it using the docker-compose-postgis.yml"
            else
            docker cp ${OPTARG} ${DB_CONTAINER_ID}:/backups/neo4j.dump
            docker stop ${DB_CONTAINER_ID}
            # Start the backup container
            docker run -it --rm --env-file ../../docker/env_files/.db_env --volume=docker_neo4j-data:/data --volume=docker_neo4j-backup:/backups neo4j/neo4j-admin neo4j-admin database load neo4j --from-path=/backups/ --verbose --overwrite-destination=true
            docker start ${DB_CONTAINER_ID}
            docker exec -it ${DB_CONTAINER_ID} bash -c 'rm /backups/neo4j.dump'
            fi
    esac
done


echo
echo "udt neo4j DB restore complete."
