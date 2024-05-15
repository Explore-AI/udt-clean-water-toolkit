# GeoServer Services

### System checks
1) Ensure that the following services are running:
    * Postgis (Populated with spatial data)
    * GeoServer
2) Ensure that the following python packages are installed:
    * geoserver-rest 
    * psycopg2-binary

   Installation can be done using: 
   ```bash
   pip3 install package-name
   ```

## Populating services

The procedure for population a GeoServer catalog involves the following
steps:

1) Creation of a new workspace.
2) Creation of a data store.
3) Publishing layers from the data store into GeoServer catalog.
4) Creating a style file for symbolising the layers published.
5) Assigning styles to the published layers.
6) Caching the styles using GWC.

The above procedure can be done of as a once off procedure or in some 
instances these can be repeated if you are intending to publish new vector
or existing dataset into a new workspace,store etc.

In our case this is a once off procedure unless the data in the database
has been updated i.e.

* New records have been added.
* Records have been deleted.
* Table definitions have been altered (Adding new column, deleting
columns, changing column data types).

### Function descriptions

We have a script `geoserver_populate_services.py` which has some
functions to allow interaction with GeoServer headless. The 
following functions are defined in the script:

1) The function `populate_geoserver` is used to run through the steps outlined from (step 1 to step 5).
2) The function `gwc_cache_all_layers` is used to initiate seeding for all the vector layer (step 6).
3) The function `gwc_cache_truncate_all_layers` is used to clean up the cache of layers. Useful when the source layers have changed in the database.
4) The function `reload_geoserver_layers` is used to reload database layers into GeoServer. Useful when the data has changed in the DB i.e. new columns added or delete.
5) The function `recalculate_layer_bbox` is used to reload the layer bounding box,useful if the data extent has changed in the database i.e. (new rows added or deleted).

### Running scripts

1) We assume you are going to have logged into the Django container
2) Run the following script 
    ```
     python3 /geoserver_scripts/geoserver_populate_services.py function_name
   ```
   where function_name can be either `populate_geoserver,gwc_cache_all_layers,gwc_cache_truncate_all_layers,reload_geoserver_layers,recalculate_layer_bbox`. If no function is given as an argument it will run `populate_geoserver`.
3) Navigate to your GeoServer instance, and you should be able to
access the layers through the various endpoints and check the services.
4) The following URL are important for the clientside rendering:
    * [MVT TMS](http://localhost:8080/geoserver/gwc/service/tms/1.0.0/udt:assets_logger@EPSG:900913@pbf/%7Bz%7D/%7Bx%7D/%7B-y%7D.pbf) 
    * [MVT GWC](http://localhost:8080/geoserver/udt/gwc/service/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&LAYER=udt:assets_hydrant&STYLE=&TILEMATRIX=EPSG:900913:8&TILEMATRIXSET=EPSG:900913&FORMAT=application/vnd.mapbox-vector-tile&TILECOL={x}&TILEROW={y})

## Generating Reports (SVG images)

We have a script `geoserver_generate_report.py` which has some
functions to allow interaction with GeoServer headless. The 
following functions are defined in the script:

1) The function `geoserver_get_map` is used to generate snapshot of layers published in GeoServer based on the extent of the layer and preferred image format (Set with an env variable OUTPUT_FORMAT).
2) The function `dma_get_map` is used to generate snapshot of layers based on the extent of a specific DMA (You need to pass
an env variable i.e. DMA_CODES=['ZWAL4801', 'ZCHESS12', 'ZCHIPO01']).

### Running scripts

1) Run the script 
    ```
    python3 /geoserver_scripts/geoserver_generate_report.py function_name
    ```
    Where function_name can be either `geoserver_get_map` or `dma_get_map`. If no argument is given the `geoserver_get_map` function will be executed.
2) Navigate to `/geoserver_scripts/output` to preview the rendered images.
