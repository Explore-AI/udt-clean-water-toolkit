#!/bin/bash

echo "Started udt postgis server setup."
echo

pushd ../docker/ || exit

docker-compose -f ../docker/docker-compose-cwa-geodjango-dev.yml up -d udtpostgis

popd ../scripts/ || exit
echo
echo "Postgis server setup complete."
