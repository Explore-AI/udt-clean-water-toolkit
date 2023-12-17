# udt-toolkit

NB: This document is a work in progress.

## 1. Overview

Development of a clean water toolkit that combines aspects of a digital twin and clean water modelling/analysis.

## 2. Project structure

### api

A FastAPI application built with SQLAlchemy. Provides a RESTful interface for the `cwm` module. Also provides additional apis for visualisation, analysis, and modelling.

### cwm

The Clean Water Module (cwm) is a python module that reads in clean water assett data (in geospatial and/or potentially other formats), performs validation and constructs a network.

## 3. Development

### api

NB: Before running the `api` for development one must create a symlink of the cwm module into the `api` directory.

```
ln -s ../cwm/src/ api/uwm
```

## 4. Deployment


