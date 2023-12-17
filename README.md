# udt-clean-water-toolkit

NB: This document is a work in progress.

## 1. Overview

Development of a clean water toolkit that combines aspects of a digital twin and clean water modelling/analysis.

## 2. Project structure

### api

A FastAPI application built with SQLAlchemy. Provides a RESTful API interface for the `cwm` module. Also provides additional apis for visualisation, analysis, and modelling.

### cwm

The Clean Water Module (cwm) is a python module/library that reads in clean water assett data (in geospatial and/or potentially other formats), performs validation and constructs a network.

### app

The primary application for Clean Water Toolkit. It utilises the `cwm` library and provides functional and class based APIs. It is non-graphical.

### api2

NB: for experimentation purposes only. A DRF application. Provides a RESTful API interface for the `cwm` module. Also provides additional apis for visualisation, analysis, and modelling. It is not for production.

### ui

An electron based app. Interacts with the `api` and provides a GUI that demonstrates some of the capabilities of the Clean Water Toolkit.

### devops

Devops tools for application development and deployment.

## 3. Development

### api

NB: Before running the `api` for development one must create a symlink of the cwm module into the `api` directory.

```
ln -s ../cwm/src/ api/cwm
```

Create a python3 virtual environment and install required modules. The necessary `cwm` modules will also need to be installed. For example using pip:

```
python3 -m venv api/venv

source api/venv/bin/activate

pip install -r api/requirements.txt

pip install -r cwm/requirements.txt
```

### app

NB: Before running the `api` for development one must create a symlink of the cwm module into the `api` directory.

```
ln -s ../cwm/src/ app/cwm
```

Create a python3 virtual environment and install required modules. The necessary `cwm` modules will also need to be installed. For example using pip:

```
python3 -m venv app/venv

source app/venv/bin/activate

pip install -r app/requirements.txt

pip install -r cwm/requirements.txt
```

## 4. Deployment


