# api_drf

## 1. Requirements

### 1.1 Packages

- Django
- djangorestframework
- django-filter
- psycopg2-binary
- python-dotenv
- cwm (from this package)

These packages can be installed with the instructions in Section 2.

`sudo apt-get install libgdal-dev`

### 1.2 Database

The following databases are suppored by GeoDjango can be used with the app*:

- SpatiaLite
- MySQL
- MariaDB
- PostGIS (recommended for use with this application)

*Please check the functions used in the application have compatability with your selected database. 

## 2. Development

Create a python3 virtual environment and install required modules. For example using pip:

```
# from project root dir

python3 -m venv api_drf/venv

source api/api_drf/venv/bin/activate

pip install -r api_drf/requirements.txt -r api_drf/dev-requirements.txt

ln -s cwa/cwa_geodjango/cwa_geod/ ./api_drf
```

Install a postgis database and expose the required port. Before running the `docker-compose` command to setup the postgis DB. you will need set the `POSTGRES_PASSWORD` env var in `devops/docker/env/.db_env`.

```
cd devops/docker/

docker-compose -f docker-compose-postgis.yml up -d
```

Before running the `api_drf` for development one needs to package and install the `cwm` module in dev mode:

```
# assuming you area already in the `api2` virtual environment

cd cwm/

pip install -e .

# The module can now be imported with

import cleanwater
```

## Helpful resources

- The [GeoDjango documentation](https://docs.djangoproject.com/en/4.2/ref/contrib/gis/). The tutorial is helpful. The Model, Database, Queryset, and GDAL APIs are used widely in this project and are useful references.
