# udt-clean-water-toolkit

NB: This document is a work in progress.

## 1. Overview

Development of a clean water toolkit that combines aspects of a digital twin and clean water modelling/analysis. The project is funded by Ofwat in collaboration with Thames Water and Severn Trent Water. The modules and applications provided in this toolkit are not for production. The toolkit is for POC purposes only.

## 2. Toolkit structure

### 2.1 `cwm` Module

The clean water module is a python package that reads in clean water assett data (in geospatial and/or potentially other formats), performs validation and constructs a network. Provides functional and class based apis for visualisation, analysis, and modelling. 

## 2.2 Applications

The `cwa_geoarm` and `cwa_geodorm` are two independent applications. They provide the same functionality.

#### cwa_geoaorm

An application of the Clean Water Toolkit with GeoAlchemy integration. Includes the `cwm` package and provides functional and class based APIs. It is packaged as a zip file. It can be unpacked and integrated into any other python project or it can be run with the provided shell commands. It is non-graphical. 

#### cwa_geodorm

An application of the Clean Water Toolkit. It uses GeoDjango as an ORM. Integrates the `cwm` package and provides functional and class based APIs. It is packaged as a zip file. It can be unpacked and integrated into any other python project or it can be run with the provided shell commands. It is non-graphical. 

### 2.3 RESTful API apps

The `api_fastapi` and `api_drf` are two independent applications. They provide the same functionality.

#### api_fastapi

An example api application built with FastAPI. Provides a RESTful API interface for the `cwa_geoaorm` application. Also provides additional apis for visualisation, analysis, and modelling.

#### api_drf

An example api application built with djangorestframework. Provides a RESTful API interface for the `cwa_geodorm` module. Also provides additional apis for visualisation, analysis, and modelling.

### 2.4 ui

An electron based app. A front-end for the RESTful apis.

### 2.5 devops

Devops tools for toolkit development and deployment.


## 3. Requirements

### cwm

- pandas
- geopandas
- numpy
- networkx

### cwa_geoaorm

pending

<!-- See [app requirements](cwa_geoaorm/README.md#1-requirements) -->

### cwa_geodorm

See [app requirements](cwa_geodorm/README.md#1-requirements)

### api_fastapi

See [fast api requirements](api_fastapi/README.md#1-requirements)

### api_drf

See [drf api requirements](api_drf/README.md#1-requirements)

### devops

- docker
- docker-compose

## 4. Development

### cwm

pending

### cwa_geoaorm

pending

<!-- See [app requirements](cwa_geoaorm/README.md#1-requirements) -->

### cwa_geodorm

See [app development instructions](cwa_geodorm/README.md#2-development)

### api_fastapi

See [fast api development instructions](api_fastapi/README.md#2-development)

### api_drf

See [drf api development instructions](drf_fastapi/README.md#2-development)


## 5. Deployment


