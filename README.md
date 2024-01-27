# udt-clean-water-toolkit

NB: This document is a work in progress.

## 1. Overview

Development of a clean water toolkit that combines aspects of a digital twin and clean water modelling/analysis. The project is funded by Ofwat in collaboration with Thames Water and Severn Trent Water. The modules and applications provided in this toolkit are not for production. The toolkit is for POC purposes only.

## 2. Toolkit structure

### 2.1 `cwm` module

The clean water module (cwm) is a python package that reads in clean water assett data (in geospatial and/or potentially other formats), performs validation and constructs a network. Provides functional and class based apis for visualisation, analysis, and modelling. 

### 2.2 `cwa` applications

The clean water applications (cwa) directory includes two independent applications: `cwa_geoalchemy` and `cwa_geodjango`. The applications provide similar functionality but use different frameworks.

#### cwa_geoalchemy

An application of the Clean Water Toolkit with GeoAlchemy integration. Includes the `cwm` package and provides functional and class based APIs. It is packaged as a zip file. It can be unpacked and integrated into any other python project or it can be run with the provided shell commands. It is non-graphical. 

#### cwa_geodjango

An application of the Clean Water Toolkit. It uses GeoDjango as an ORM. Integrates the `cwm` package and provides functional and class based APIs. It is packaged as a zip file. It can be unpacked and integrated into any other python project or it can be run with the provided shell commands. It is non-graphical. 

### 2.3 RESTful API apps

The `api` directory includes two independent RESTful api applications: `api_fastapi` and `api_drf`. They provide similar functionality but use different frameworks.

#### api_fastapi

An example api application built with FastAPI. Provides a RESTful API interface for the `cwa_geoaorm` app. Also provides additional apis for visualisation, analysis, and modelling.

#### api_drf

An example api application built with djangorestframework. Provides a RESTful API interface for the `cwa_geodorm` app. Also provides additional apis for visualisation, analysis, and modelling.

### 2.4 ui

An electron based app. A front-end for the RESTful apis.

### 2.5 devops

Devops tools for toolkit development and deployment.


## 3. Requirements

### 3.1 `cwm` module

See [cleanwater module requirements](cwm/README.md#1-requirements)

### 3.2 `cwa` applications

#### cwa_geoalchemy

pending

<!-- See [app requirements](cwa_geoaorm/README.md#1-requirements) -->

#### cwa_geodjango

See [app requirements](cwa/cwa_geodjango/README.md#1-requirements)

### 3.3 `api` applications

#### api_fastapi

See [fast api requirements](api/api_fastapi/README.md#1-requirements)

#### api_drf

See [drf api requirements](api/api_drf/README.md#1-requirements)

### 3.4 devops

- docker
- docker-compose

## 4. Development

### cwm

See [cleanwater module development instructions](cwm/README.md#2-development)

### cwa_geoalchemy

pending

<!-- See [app requirements](cwa_geoaorm/README.md#1-requirements) -->

### cwa_geodjango

See [app development instructions](cwa/cwa_geodjango/README.md#2-development)

### api_fastapi

See [fast api development instructions](api/api_fastapi/README.md#2-development)

### api_drf

See [drf api development instructions](api/drf_fastapi/README.md#2-development)


## 5. Tests


## 6. Build and deployment


