# GeoServer Services

### System checks
1) Ensure that the following services are running:
    * Postgis (Populated with spatial data)
    * GeoServer
2) Ensure that the following python packages are installed:
    * geoserver-rest 
    * psycopg2-binary

## Populating services

**Note** This is a once off unless that data has changed i.e.
* New records have been added
* Records have been deleted
* Table definitions have been altered (Adding new column, deleting
columns, changing column data types)

1) We assume you are going to have logged into the Django container
2) Run the following script `python3 /geoserver_scripts/geoserver_populate_services.py`.
3) Navigate to your GeoServer instance, and you should be able to
access the layers through the various endpoints.
4) The following URL are important for the clientside rendering:
    * [MVT TMS](http://localhost:8080/geoserver/gwc/service/tms/1.0.0/udt:assets_logger@EPSG:900913@pbf/%7Bz%7D/%7Bx%7D/%7B-y%7D.pbf) 
    * [MVT GWC](http://localhost:8080/geoserver/udt/gwc/service/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&LAYER=udt:assets_hydrant&STYLE=&TILEMATRIX=EPSG:900913:8&TILEMATRIXSET=EPSG:900913&FORMAT=application/vnd.mapbox-vector-tile&TILECOL={x}&TILEROW={y})

## Generating SVG

Two functions are given for generating scripts
* geoserver_get_map - Will retrieve SVG images of the full layer.
* dma_get_map - Will retrieve svg images based on a particular DMA. (You need to pass
an env variable i.e. DMA_CODES=['ZWAL4801', 'ZCHESS12', 'ZCHIPO01'])

1) Run the script `python3 /geoserver_scripts/geoserver_generate_report.py`
2) Navigate to `/geoserver_scripts/output` to preview the rendered images.

# TODO: Update documentation on how to run each function