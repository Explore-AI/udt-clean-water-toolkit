#!/bin/bash

echo "Setting up the cwa_geodjango app for development."
echo "The following actions will take place:"
echo "udt postgis server will be setup."
echo "A udt postgis database will be created."
echo "A udt superuser will be created on the postgis database."
echo "pip packages will be installed for the cwa_geodjango app."
echo "pip packages will be installed for the cwm in dev mode."
echo

docker-compose -f ../docker/docker-compose-postgis.yml -f ../docker/docker-compose-cwa-geodjango-dev.yml up -d

CWA_GEODORM_CONTAINER_ID=`docker ps | grep udtcwageodjangodev | grep cwa_geodjango_dev | awk '{ print $1 }'`

docker exec -it ${CWA_GEODORM_CONTAINER_ID} pip install -r requirements.txt -r dev-requirements.txt

docker exec -it ${CWA_GEODORM_CONTAINER_ID} pip install -e ../../cwm/

./postgis_db_init.sh

#docker exec -it ${CWA_GEODORM_CONTAINER_ID} python3 main.py migrate

echo
echo "cwa_geodjango app dev setup complete."
