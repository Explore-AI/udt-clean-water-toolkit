# api2

## 1. Requirements

### 1.1 Packages

- Django
- djangorestframework
- django-filter
- psycopg2-binary
- python-dotenv
- cwm (from this package)

These packages can be installed with the instructions in Section 2.

### 1.2 Database

The following databases are suppored by GeoDjango can be used with the app:

- SpatiaLite
- MySQL
- MariaDB
- PostGIS (recommended for use with this application)

## 2. Development

Create a python3 virtual environment and install required modules. For example using pip:

```
# from project root dir

python3 -m venv api/venv

source api2/venv/bin/activate

pip install -r api2/requirements.txt

pip install -r api2/dev-requirements.txt # for dev packages

ln -s ../app/ ./api2/
```

Install a postgis database and expose the required port

```
docker run --name udtpostgis -e POSTGRES_USER=udt -e POSTGRES_PASSWORD=[somepassword] -v /opt/udt/data/pgdata:/var/lib/postgresql/data -d postgis/postgis
```

Before running the `api2` for development one needs to package and install the `cwm` module in dev mode:

```
# assuming you area already in the `api2` virtual environment

cd cwm/

pip install -e .

# The module can now be imported with

import cleanwater
```

## Helpful resources

- The [GeoDjango documentation](https://docs.djangoproject.com/en/4.2/ref/contrib/gis/). The tutorial is helpful. The Model, Database, Queryset, and GDAL APIs are used widely in this project and are useful references.
