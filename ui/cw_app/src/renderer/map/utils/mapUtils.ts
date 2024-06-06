import { GEOSERVER_URL } from '../../config';
import { MapViewState } from '@deck.gl/core';
import { MVTLayer } from '@deck.gl/geo-layers';
import {colorCategories, colorContinuous} from '@deck.gl/carto';
import { map as _map, isEmpty as _isEmpty } from 'lodash';

export type LayerNames = {
    [key: string]: string;
};

export type LayerColorCodes = {
    [key: string]: number[];
};

export type LayerKey = keyof typeof LAYER_NAME_COLOR_CODES;

export const MVT_LAYER_URL = (asset_name: string) => {
    return `${GEOSERVER_URL}/geoserver/gwc/service/tms/1.0.0/udt:${asset_name}@EPSG:3857@pbf/{z}/{x}/{-y}.pbf`;
};

export const MAP_LAYERS_PROPS = [
    {
        visible: true,
        label: 'Chambers',
        key: 'assets_chamber',
        assetType: 'point',
        colorCode: [245, 183, 177],
    },
    {
        visible: false,
        label: 'Distribution Main',
        key: 'assets_distributionmain',
        assetType: 'line',
        colorCode: [162, 217, 206],
    },
    {
        visible: true,
        label: 'Hydrants',
        key: 'assets_hydrant',
        assetType: 'point',
        colorCode: [0, 158, 222],
    },
    {
        visible: true,
        label: 'Loggers',
        key: 'assets_logger',
        assetType: 'point',
        colorCode: [249, 231, 159],
    },
    {
        visible: true,
        label: 'Network Meter',
        key: 'assets_networkmeter',
        assetType: 'point',
        colorCode: [88, 214, 141],
    },
    {
        visible: true,
        label: 'Network Opt Valve',
        key: 'assets_networkoptvalve',
        assetType: 'point',
        colorCode: [165, 105, 189],
    },
    {
        visible: true,
        label: 'Operational Site',
        key: 'assets_operationalsite',
        assetType: 'point',
        colorCode: [165, 105, 189],
    },
    {
        visible: true,
        label: 'Pressure Control Valve',
        key: 'assets_pressurecontrolvalve',
        assetType: 'point',
        colorCode: [211, 84, 0],
    },
    {
        visible: true,
        label: 'Pressure Fitting',
        key: 'assets_pressurefitting',
        assetType: 'point',
        colorCode: [74, 35, 90],
    },
    {
        visible: false,
        label: 'Trunk Main',
        key: 'assets_trunkmain',
        assetType: 'line',
        colorCode: [33, 97, 140],
    },
    {
        visible: true,
        label: 'DMA',
        key: 'utilities_dma',
        assetType: 'polygon',
        colorCode: [8, 48, 107],//'#08306b',
        opacity: 0.1
    },
];

export const DEFAULT_BASEMAP_PROPS = [
    {
        visible: true,
        label: 'Open Street Map',
        mapUrl: 'mapbox://styles/mapbox/streets-v12',
        key: 'open_street_map',
    },
    {
        visible: false,
        label: 'Satellite Map',
        mapUrl: 'mapbox://styles/mapbox/satellite-v9',
        key: 'satellite_map',
    },
    {
        visible: false,
        label: 'Dark Map',
        mapUrl: 'mapbox://styles/mapbox/dark-v11',
        key: 'dark_map',
    },
    {
        visible: false,
        label: 'Terrain',
        mapUrl: 'mapbox://styles/mapbox/outdoors-v12',
        key: 'terrain_map',
    },
];

export const gpsRegex =
    /^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?((1[0-7]\d(\.\d+)?|180(\.0+)?)|(\d{1,2}(\.\d+)?))$/;
export const gisidRegex = /^\d{7}$/;

export const COMMON_STYLING = {
    opacity: 0.1
}

export const POINT_STYLING = {
    ...COMMON_STYLING,
    getFillColor: [1,1,1],
}

export const LINE_STYLING = {
    ...COMMON_STYLING,
    getFillColor: [1,1,1],
}

export const POLYGON_STYLING = {
    ...COMMON_STYLING,
    getFillColor: colorCategories({
        attr: 'code',
        domain: ['ZABINB01', 'ZABIND03', 'ZCHIPO01', 'mid and military', 'ZABIND08'],// TODO: get dmas from from geoserverb
        colors: 'BluYl'
    }),
}


export const createLayers = (newMapLayerProps = []) => {
    const mapLayerProps = !_isEmpty(newMapLayerProps)? newMapLayerProps: MAP_LAYERS_PROPS;

    return _map(mapLayerProps, (layerProps) => {

        let layerStyle = COMMON_STYLING
        if (layerProps.assetType === 'point') {
            layerStyle = POINT_STYLING
        } else if (layerProps.assetType === 'line') {
            layerStyle = LINE_STYLING
        } else if (layerProps.assetType === 'polygon') {
            layerStyle = POLYGON_STYLING
        }

        return new MVTLayer({
            pickable: true,
            id: layerProps.key,
            data: [MVT_LAYER_URL(layerProps.key)],
            visible: layerProps.visible,
            ...layerStyle
        });
    });
};
