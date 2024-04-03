
#!/bin/bash

apt update;apt-get -y --no-install-recommends install python3-pip

pip3 install geoserver-rest psycopg2-binary

# Generate and populate services
python3 /geoserver/geoserver_populate_services.py

# Download images in your preferred format. If you need to adjust params, change default params in script
python3 /geoserver/geoserver_generate_report.py