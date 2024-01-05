# cleanwater module

## 1. Requirements

### 1.1 Packages

- geopandas
- numpy
- momepy
- matplotlib
- networkx

These packages can be installed with the instructions in Section 2.


## 2. Development

### 2.1 Package installation

Create a python3 virtual environment and install required modules. For example using pip:

```
# from project root dir

python3 -m venv cwa_geodorm/venv

source cwa_geodorm/venv/bin/activate

pip install -r requirements.txt -r dev-requirements.txt
```

Before running the `cwa_geodorm` for development one needs to package and install the `cwm` module in dev mode:

```
# assuming you area already in the `cwa_geodorm` virtual environment

cd cwm/

pip install -e .

# The module can now be imported with

import cleanwater
```

### 2.2 Postgis DB setup 

Install a postgis database and expose the required port. Before running the `docker-compose` command to setup the postgis DB. you will need set the `POSTGRES_PASSWORD` env var in `devops/docker/env/.db_env`.

```
cd devops/docker/

docker-compose -f docker-compose-postgis.yml up -d
```

## Helpful resources

- The [GeoDjango documentation](https://docs.djangoproject.com/en/4.2/ref/contrib/gis/). The tutorial is helpful. The Model, Database, Queryset, and GDAL APIs are used widely in this project and are useful references.
