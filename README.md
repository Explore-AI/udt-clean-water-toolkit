# udt-clean-water-toolkit

NB: This document is a work in progress.

## 1. Overview

Development of a clean water toolkit that combines aspects of a digital twin and clean water modelling/analysis. The project is funded by Ofwat in collaboration with Thames Water and Severn Trent Water. The modules and applications provided in this toolkit are not for production. The toolkit is for POC purposes only.

## 2. Project structure

### cwm

The clean water module is a python package/module that reads in clean water assett data (in geospatial and/or potentially other formats), performs validation and constructs a network. Provides functional and class based apis for visualisation, analysis, and modelling. 

### cwa_geoaorm

An application of the Clean Water Toolkit. Integrates the `cwm` package and provides functional and class based APIs. It is packaged as a zip file. It can be unpacked and integrated into any other python project or it can be run with the provided shell commands. It is non-graphical. 

### cwa_geodorm

An application of the Clean Water Toolkit. It uses GeoDjango as an ORM. Integrates the `cwm` package and provides functional and class based APIs. It is packaged as a zip file. It can be unpacked and integrated into any other python project or it can be run with the provided shell commands. It is non-graphical. 

### api_fastapi

An example api application built with FastAPI application SQLAlchemy. Provides a RESTful API interface for the `cwa_geoaorm` application. Also provides additional apis for visualisation, analysis, and modelling.

### api_drf

An example api application built with djangorestframework. Provides a RESTful API interface for the `cwa_geodorm` module. Also provides additional apis for visualisation, analysis, and modelling.

### ui

An electron based app. Commincates with the apis Clean Water ToolkitInteracts with the `api` and RESTFul APIs and provides a graphicainterface that demonstrates some of the Toolkit capabilities.

### devops

Devops tools for toolkit development and deployment.


## 3. Requirements

### api

See [api requirements](api/README.md#1-requirements)

### api2

See [api2 requirements](api2/README.md#1-requirements)

### cwm

- pandas
- geopandas
- numpy
- networkx

### app

See [app requirements](app/README.md#1-requirements)

### devops

- docker
- docker-compose


## 4. Development

### api

See [api development instructions](api/README.md#2-development)

### api2

See [api2 development instructions](api2/README.md#2-development)

### app

See [app development instructions](app/README.md#2-development)

## 5. Deployment


