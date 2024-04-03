#!/bin/bash

echo "Setting up the cwa_geodjango app for development."
echo "The following actions will take place:"
echo "udt postgis server will be setup."
echo "A udt postgis database will be created."
echo "A udt superuser will be created on the postgis database."
echo "pip packages will be installed for the cwa_geodjango app."
echo "pip packages will be installed for the cwm in dev mode."
echo


docker compose -f ../docker/docker-compose-postgis.yml -f ../docker/docker-compose-neo4j.yml -f ../docker/docker-compose-cwa-geodjango-dev.yml -f ../docker/docker-compose-cwa-geoalchemy-dev.yml -f ../docker/docker-compose-geoserver.yml up -d --build

CWA_GEODORM_CONTAINER_ID=`docker ps | grep udtcwageodjangodev | grep cwa_geodjango_dev | awk '{ print $1 }'`
CWA_GEOALCHEMY_CONTAINER_ID=`docker ps | grep udtcwageoalchemydev | grep cwa_geoalchemy_dev | awk '{ print $1 }'`
CWA_GEOSERVER_CONTAINER_ID=`docker ps | grep udtgeoserver | grep kartoza/geoserver:2.25.0 | awk '{ print $1 }'`

docker exec -it ${CWA_GEODORM_CONTAINER_ID} pip install -r requirements.txt -r dev-requirements.txt

docker exec -it ${CWA_GEOALCHEMY_CONTAINER_ID} pip install -r requirements.txt

docker exec -it ${CWA_GEODORM_CONTAINER_ID} pip install -e ../../cwm/

./postgis/postgis_db_init.sh

#docker exec -it ${CWA_GEODORM_CONTAINER_ID} python3 main.py migrate

docker exec -it ${CWA_GEODORM_CONTAINER_ID} /bin/bash /geoserver/geoserver_import.sh
echo
echo "cwa_geodjango app dev setup complete."
echo "cwa_geoalchemy app dev setup complete."
echo "GeoServer app setup complete."