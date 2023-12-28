# api_fastapi

## 1. Requirements

- FastAPI
- pydantic
- uvicorn
- SQLAlchemy
- alembic
- python-dotenv
- cwm (from this package)

These packages can be installed with the instructions in Section 2.

## 2. Development

Create a python3 virtual environment and install required modules. For example using pip:

```
# from project root dir

python3 -m venv api/venv

source api/venv/bin/activate

pip install -r api/requirements.txt -r api/dev-requirements.txt # for dev packages
```

Install a postgis database and expose the required port. Before running the `docker-compose` command to setup the postgis DB. you will need set the `POSTGRES_PASSWORD` env var in `devops/docker/env/.db_env`.

```
cd devops/docker/

docker-compose -f docker-compose-postgis.yml up -d
```

Before running the `api_fastapi` for development one needs to package and install the `cwm` module in dev mode:

```
# assuming you area already in the `api` virtual environment

cd cwm/

pip install -e .

# The module can now be imported with

import cleanwater
```

