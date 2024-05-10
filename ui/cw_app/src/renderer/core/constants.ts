import 'dotenv';

export const MAPBOX_TOKEN = process.env.MAPBOX_TOKEN;

export type LayerNames = {
    [key: string]: string;
};

export type LayerColorCodes = {
    [key: string]: number[];
};

export const LAYER_NAMES = {
    chambers: 'assets_chamber',
    distribution_main: 'assets_distributionmain',
    hydrants: 'assets_hydrant',
    loggers: 'assets_logger',
    network_meter: 'assets_networkmeter',
    network_opt_valve: 'assets_networkoptvalve',
    operational_site: 'assets_operationalsite',
    pressure_control_valve: 'assets_pressurecontrolvalve',
    pressure_fitting: 'assets_pressurefitting',
    trunkmain: 'assets_trunkmain',
};

export const LAYER_NAME_COLOR_CODES = {
    chambers: [245, 183, 177],
    distribution_main: [162, 217, 206],
    hydrants: [0, 158, 222],
    loggers: [249, 231, 159],
    network_meter: [88, 214, 141],
    network_opt_valve: [165, 105, 189],
    operational_site: [165, 105, 189],
    pressure_control_valve: [211, 84, 0],
    pressure_fitting: [74, 35, 90],
    trunkmain: [33, 97, 140],
};

export const MVT_LAYER_URL = (asset_name: string) => {
    return `http://localhost:8080/geoserver/gwc/service/tms/1.0.0/udt:${asset_name}@EPSG:900913@pbf/{z}/{x}/{-y}.pbf`;
};

export const MVT_LAYER_URL_TWO = (asset_name: string) => {
    return `http://localhost:8080/geoserver/udt/gwc/service/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&LAYER=udt:${asset_name}&STYLE=&TILEMATRIX=EPSG:900913:13&TILEMATRIXSET=EPSG:900913&FORMAT=application/vnd.mapbox-vector-tile&TILECOL={x}&TILEROW={y}`;
};
