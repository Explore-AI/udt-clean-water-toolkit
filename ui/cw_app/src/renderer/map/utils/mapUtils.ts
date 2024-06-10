import { MapViewState } from '@deck.gl/core';
import { MVTLayer } from '@deck.gl/geo-layers';
import { colorCategories } from '@deck.gl/carto';
import { map as _map, isEmpty as _isEmpty } from 'lodash';
import { GEOSERVER_URL } from '../../config';

export type LayerNames = {
    [key: string]: string;
};

export type LayerColorCodes = {
    [key: string]: number[];
};

export const MVT_LAYER_URL = (asset_name: string) => {
    return `${GEOSERVER_URL}/geoserver/gwc/service/tms/1.0.0/udt:${asset_name}@EPSG:3857@pbf/{z}/{x}/{-y}.pbf`;
};

export const MAP_LAYERS_PROPS = [
    {
        visible: true,
        label: 'Chambers',
        key: 'assets_chamber',
        assetType: 'point',
    },
    {
        visible: false,
        label: 'Distribution Main',
        key: 'assets_distributionmain',
        assetType: 'line',
    },
    {
        visible: true,
        label: 'Hydrants',
        key: 'assets_hydrant',
        assetType: 'point',
    },
    {
        visible: true,
        label: 'Loggers',
        key: 'assets_logger',
        assetType: 'point',
    },
    {
        visible: true,
        label: 'Network Meter',
        key: 'assets_networkmeter',
        assetType: 'point',
    },
    {
        visible: true,
        label: 'Network Opt Valve',
        key: 'assets_networkoptvalve',
        assetType: 'point',
    },
    {
        visible: true,
        label: 'Operational Site',
        key: 'assets_operationalsite',
        assetType: 'point',
    },
    {
        visible: true,
        label: 'Pressure Control Valve',
        key: 'assets_pressurecontrolvalve',
        assetType: 'point',
    },
    {
        visible: true,
        label: 'Pressure Fitting',
        key: 'assets_pressurefitting',
        assetType: 'point',
    },
    {
        visible: false,
        label: 'Trunk Main',
        key: 'assets_trunkmain',
        assetType: 'line',
    },
    {
        visible: true,
        label: 'DMA',
        key: 'utilities_dma',
        assetType: 'polygon',
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

function getFillColorFeatures(feature, colorMap) {
    const { property } = colorMap;
    const value = feature.properties[property];
    return colorMap.colors[value] || colorMap.default;
}

const AssetsPressurefittingColormap = {
    property: 'subtype',
    colors: {
        tapping_point: [220, 215, 71],
        telemetry_pit: [15, 24, 255, 128],
        transducer: [0, 0, 255, 128],
    },
    default: [0, 255, 0, 128],
};

const AssetsChamberColormap = {
    property: 'gid',
    colors: {
        Null: [220, 215, 71],
    },
    default: [76, 43, 50, 1],
};

const AssetsHydrantColormap = {
    property: 'gid',
    colors: {
        Null: [220, 215, 71],
    },
    default: [145, 82, 45, 1],
};

const AssetsLoggerColormap = {
    property: 'gid',
    colors: {
        Null: [220, 215, 71],
    },
    default: [100, 81, 44, 1],
};

const AssetsNetworkmeterColormap = {
    property: 'subtype',
    colors: {
        distribution_input_meter: [220, 212, 71],
        district_meter: [146, 24, 17, 128],
        fire_meter: [10, 0, 77, 128],
        unknown: [80, 102, 200, 128],
        waste_meter: [90, 40, 120, 128],
        zonal_meter: [60, 50, 133, 128],
    },
    default: [0, 255, 0, 128],
};

const AssetsNetworkoptvalveColormap = {
    property: 'gid',
    colors: {
        Null: [220, 215, 71],
    },
    default: [88, 43, 50, 1],
};

const AssetsOperationalsiteColormap = {
    property: 'subtype',
    colors: {
        booster_station: [128, 233, 102],
        borehole: [61, 202, 164],
        break_pressure_tank: [209, 212, 38],
        other: [130, 222, 157],
        pumping_station: [174, 214, 126],
        raw_water_storage_reservoir: [117, 157, 218],
        reservoir_covered: [59, 195, 225],
        service_reservoir: [237, 47, 95],
        shaft_inspection: [108, 103, 231],
        shaft_pumping: [232, 194, 236],
        treatment_works: [236, 42, 174],
        unknown: [201, 109, 213],
        water_tower: [162, 96, 237],
    },
    default: [0, 255, 0, 128],
};

const AssetsPressurecontrolvalveColormap = {
    property: 'subtype',
    colors: {
        needle: [211, 223, 45],
        non_return_valve: [202, 79, 73],
        plug_valve: [41, 29, 221],
        pressure_reducing: [240, 144, 234],
        pressure_sustaining: [77, 198, 207],
    },
    default: [0, 255, 0, 128],
};


function AssetsPressurecontrolvalveFillcolor(feature) {
    return getFillColorFeatures(feature, AssetsPressurefittingColormap);
}

function AssetsChamberFillcolor(feature) {
    return getFillColorFeatures(feature, AssetsChamberColormap);
}

function AssetsHydrantFillcolor(feature) {
    return getFillColorFeatures(feature, AssetsHydrantColormap);
}

function AssetsLoggerFillcolor(feature) {
    return getFillColorFeatures(feature, AssetsLoggerColormap);
}

function AssetsNetworkmeterFillcolor(feature) {
    return getFillColorFeatures(feature, AssetsNetworkmeterColormap);
}

function AssetsNetworkoptvalveFillcolor(feature) {
    return getFillColorFeatures(feature, AssetsNetworkoptvalveColormap);
}

function AssetsOperationalsiteFillcolor(feature) {
    return getFillColorFeatures(feature, AssetsOperationalsiteColormap);
}

function AssetsPressureControlValveFillcolor(feature) {
    return getFillColorFeatures(feature, AssetsPressurecontrolvalveColormap);
}

export const COMMON_STYLING = {
    minZoom: 8,
    maxZoom: 18,
};

export const POINT_STYLING = (AssetName: string) => {
    let styling = '';
    let AssetsValues = [
        'assets_pressurefitting',
        'assets_chamber',
        'assets_hydrant',
        'assets_logger',
        'assets_networkmeter',
        'assets_networkoptvalve',
        'assets_operationalsite',
        'assets_pressurecontrolvalve',
    ];

    if (AssetName === 'assets_pressurefitting') {
        styling = AssetsPressurecontrolvalveFillcolor;
    } else if (AssetName === 'assets_chamber') {
        styling = AssetsChamberFillcolor;
    } else if (AssetName === 'assets_hydrant') {
        styling = AssetsHydrantFillcolor;
    } else if (AssetName === 'assets_logger') {
        styling = AssetsLoggerFillcolor;
    } else if (AssetName === 'assets_networkmeter') {
        styling = AssetsNetworkmeterFillcolor;
    } else if (AssetName === 'assets_networkoptvalve') {
        styling = AssetsNetworkoptvalveFillcolor;
    } else if (AssetName === 'assets_operationalsite') {
        styling = AssetsOperationalsiteFillcolor;
    } else if (AssetName === 'assets_pressurecontrolvalve') {
        styling = AssetsPressureControlValveFillcolor;
    }
    return {
        ...COMMON_STYLING,
        radiusMinPixels: 6,
        radiusMaxPixels: 10,
        getPointRadius: 20,
        getFillColor: f => styling(f),
    };
};
export const LINE_STYLING = (AssetName: string) => {
    let ColorValue: number[] = [];
    if (AssetName === 'assets_distributionmain') {
        ColorValue = [228, 135, 60];
    } else if (AssetName === 'assets_trunkmain') {
        ColorValue = [72, 123, 182];
    }

    return {
        ...COMMON_STYLING,
        getLineColor: ColorValue,
        lineWidthMinPixels: 1.5,
        stroked: false,
    };
};

export const POLYGON_STYLING = {
    ...COMMON_STYLING,
    opacity: 0.1,
    getFillColor: colorCategories({
        attr: 'code',
        domain: ['ZABINB01', 'ZABIND03', 'ZCHIPO01', 'ZABIND08'], // TODO: get dmas from from geoserver
        colors: 'BluYl',
        othersColor: [72, 123, 182],
    }),
};

export const createLayers = (newMapLayerProps = []) => {
    const mapLayerProps = !_isEmpty(newMapLayerProps)? newMapLayerProps: MAP_LAYERS_PROPS;

    return _map(mapLayerProps, (layerProps) => {

        let layerStyle = COMMON_STYLING
        if (layerProps.assetType === 'point') {
            layerStyle = POINT_STYLING(layerProps.key);
        } else if (layerProps.assetType === 'line') {
            layerStyle = LINE_STYLING(layerProps.key);
        } else if (layerProps.assetType === 'polygon') {
            layerStyle = POLYGON_STYLING;
        }

        return new MVTLayer({
            pickable: true,
            id: layerProps.key,
            data: [MVT_LAYER_URL(layerProps.key)],
            visible: layerProps.visible,
            ...layerStyle,
        });
    });
};
