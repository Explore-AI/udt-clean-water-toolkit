NB: This package is a module that can be run independently as well as within another project. Therefore, use relative imports only

# app

## 1. Requirements

- tbc
- cwm (from this package)

These packages can be installed with the instructions in Section 2.

## 2. Development

Create a python3 virtual environment and install required modules. For example using pip:

```
# from project root dir

python3 -m venv api/venv

source app/venv/bin/activate

pip install -r app/requirements.txt

pip install -r app/dev-requirements.txt # for dev packages

ln -s ../app/ ./app/
```

Install a postgis database and expose the required port

```
docker run --name udtpostgis -e POSTGRES_USER=udt -e POSTGRES_PASSWORD=[somepassword] -v /opt/udt/data/pgdata:/var/lib/postgresql/data -d postgis/postgis
```

Before running the `app` for development one needs to package and install the `cwm` module in dev mode:

```
# assuming you area already in the `app` virtual environment

cd cwm/

pip install -e .

# The module can now be imported with

import cleanwater
```




