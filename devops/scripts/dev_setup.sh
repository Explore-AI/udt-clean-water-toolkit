#!/bin/bash

echo "Setting up the cwa_geodjango app for development."
echo "The following actions will take place:"
echo "udt postgis server will be setup."
echo "A udt postgis database will be created."
echo "A udt superuser will be created on the postgis database."
echo "pip packages will be installed for the cwa_geodjango app."
echo "pip packages will be installed for the cwm in dev mode."
echo

# Usage ./dev_setup.sh $1 where $1 is the version of docker-compose in use i.e ./dev_setup.sh docker-compose

VERSION='docker compose'

if [ -n "$1" ]; then
    VERSION=$1
fi

pushd ../docker/ || exit

${VERSION} -f docker-compose-cwa-geodjango-dev.yml up -d --build

# TODO Add the below commands to dockerfile and run as build step
${VERSION} -f docker-compose-cwa-geodjango-dev.yml exec cwageodjangodev pip install -r requirements.txt -r dev-requirements.txt

${VERSION} -f docker-compose-cwa-geodjango-dev.yml exec  cwageodjangodev pip install -e ../../cwm/

#${VERSION} -f docker-compose-cwa-geodjango-dev exec -it cwageodjangodev python3 main.py migrate
popd ../scripts/ || exit
echo
echo "cwa_geodjango app dev setup complete."
