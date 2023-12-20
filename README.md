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

See [api requirements](api/README.md)

### api2

See [api2 requirements](api2/README.md)

### cwm

- pandas
- geopandas
- numpy
- networkx

### app

See [app requirements](app/README.md)

### devops

- docker
- docker-compose


## 4. Development

### api

See [api development instructions](api/README.md)

### api2

See [api2 development instructions](api2/README.md)

### app

See [app development instructions](app/README.md)

## 5. Deployment


