# udt-clean-water-toolkit

NB: This document is a work in progress.

## 1. Overview

Development of a clean water toolkit that combines aspects of a digital twin and clean water modelling/analysis. The project is funded by Ofwat in collaboration with Thames Water and Severn Trent Water.

## 2. Project structure

### api

A FastAPI application built with SQLAlchemy. Provides a RESTful API interface for the `cwm` module. Also provides additional apis for visualisation, analysis, and modelling.

### cwm

The clean water module is a python module/library that reads in clean water assett data (in geospatial and/or potentially other formats), performs validation and constructs a network.

### app

The primary application for Clean Water Toolkit. It utilises the `cwm` library and provides functional and class based APIs. It is packaged into a single distributable and can be imported into other .py files or run with the provided shell commands. It is non-graphical. 

### api2

NB: for experimentation purposes only. A DRF application. Provides a RESTful API interface for the `cwm` module. Also provides additional apis for visualisation, analysis, and modelling. It is not for production.

### ui

An electron based app. Interacts with the `api` and provides a GUI that demonstrates some of the capabilities of the Clean Water Toolkit.

### devops

Devops tools for toolkit development and deployment.


## 3. Requirements

### api

- FastAPI
- pydantic
- uvicorn
- SQLAlchemy
- alembic

### cwm

- pandas
- geopandas
- numpy
- networkx

### app

- SQLAlchemy
- alembic

### devops

- docker
- docker-compose


## 4. Development

### api

Create a python3 virtual environment and install required modules. For example using pip:

```
# from project root dir

python3 -m venv api/venv

source api/venv/bin/activate

pip install -r api/requirements.txt

ln -s ../app/ ./api/
```

Before running the `api` for development one needs to package and install the `cwm` module in dev mode:

```
# assuming you area already in the `api` virtual environment

cd cwm/

pip install -e .
```

### api2

Create a python3 virtual environment and install required modules. For example using pip:

```

# from project root dir

python3 -m venv api/venv

source api2/venv/bin/activate

pip install -r api2/requirements.txt

pip install -r api2/dev-requirements.txt # for dev packages

ln -s ../app/ ./api2/
```

Before running the `api` for development one needs to package and install the `cwm` module in dev mode:

```
# assuming you area already in the `api2` virtual environment

cd cwm/

pip install -e .
```


### app

Create a python3 virtual environment and install required modules. For example using pip:

```
python3 -m venv app/venv

source app/venv/bin/activate

pip install -r app/requirements.txt
```

Before running the `app` for development one needs to package and install the `cwm` module in dev mode:

```
# assuming you area already in the `app` virtual environment

cd cwm/

pip install -e .
```

## 5. Deployment


