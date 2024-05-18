import { GEOSERVER_URL } from '../config';
import { MapViewState } from '@deck.gl/core';

export type LayerNames = {
    [key: string]: string;
};

export type LayerColorCodes = {
    [key: string]: number[];
};

export type LayerKey = keyof typeof LAYER_NAME_COLOR_CODES;

export const MVT_LAYER_URL = (asset_name: string) => {
    return `${GEOSERVER_URL}/geoserver/gwc/service/tms/1.0.0/udt:${asset_name}@EPSG:900913@pbf/{z}/{x}/{-y}.pbf`;
};

export const MVT_LAYER_URL_TWO = (asset_name: string) => {
    return `${GEOSERVER_URL}/geoserver/udt/gwc/service/wmts?REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&LAYER=udt:${asset_name}&STYLE=&TILEMATRIX=EPSG:900913:13&TILEMATRIXSET=EPSG:900913&FORMAT=application/vnd.mapbox-vector-tile&TILECOL={x}&TILEROW={y}`;
};

export const MAP_LAYERS_INFO = [
    {
        visible: false,
        label: 'Chambers',
        key: 'assets_chamber',
        colorCode: [245, 183, 177],
    },
    {
        visible: false,
        label: 'Distribution Main',
        key: 'assets_distributionmain',
        colorCode: [162, 217, 206],
    },
    {
        visible: false,
        label: 'Hydrants',
        key: 'assets_hydrant',
        colorCode: [0, 158, 222],
    },
    {
        visible: false,
        label: 'Loggers',
        key: 'assets_logger',
        colorCode: [249, 231, 159],
    },
    {
        visible: false,
        label: 'Network Meter',
        key: 'assets_networkmeter',
        colorCode: [88, 214, 141],
    },
    {
        visible: false,
        label: 'Network Opt Valve',
        key: 'assets_networkoptvalve',
        colorCode: [165, 105, 189],
    },
    {
        visible: false,
        label: 'Operational Site',
        key: 'assets_operationalsite',
        colorCode: [165, 105, 189],
    },
    {
        visible: false,
        label: 'Pressure Control Valve',
        key: 'assets_pressurecontrolvalve',
        colorCode: [211, 84, 0],
    },
    {
        visible: false,
        label: 'Pressure Fitting',
        key: 'assets_pressurefitting',
        colorCode: [74, 35, 90],
    },
    {
        visible: false,
        label: 'Trunk Main',
        key: 'assets_trunkmain',
        colorCode: [33, 97, 140],
    },
];

export const DEFAULT_BASEMAP_TOGGLE = [
    {
        visible: true,
        label: 'Open Street Map',
        map_url: 'mapbox://styles/mapbox/streets-v12',
        key: 'open_street_map',
    },
    {
        visible: false,
        label: 'Satellite Map',
        map_url: 'mapbox://styles/mapbox/satellite-v9',
        key: 'satellite_map',
    },
    {
        visible: false,
        label: 'Dark Map',
        map_url: 'mapbox://styles/mapbox/dark-v11',
        key: 'dark_map',
    },
    {
        visible: false,
        label: 'Terrain',
        map_url: 'mapbox://styles/mapbox/outdoors-v12',
        key: 'terrain_map',
    },
];

export const INITIAL_VIEW_STATE: MapViewState = {
    longitude: -0.118092,
    latitude: 51.5074,
    zoom: 10,
    bearing: 0,
    pitch: 30,
};
