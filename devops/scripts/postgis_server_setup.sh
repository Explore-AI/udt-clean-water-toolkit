#!/bin/bash

echo "Started udt postgis server setup."

docker-compose -f ../docker/docker-compose-postgis.yml up -d

echo "Postgis server setup complete."
