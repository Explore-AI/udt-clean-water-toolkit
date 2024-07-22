import { MapViewState } from '@deck.gl/core';
import { MVTLayer } from '@deck.gl/geo-layers';
import { IconLayer } from '@deck.gl/layers';
import { colorCategories } from '@deck.gl/carto';
import { map as _map, isEmpty as _isEmpty } from 'lodash';
import {GEOSERVER_ADMIN_PASSWORD, GEOSERVER_URL} from '../../config';

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
        visible: true,
        label: 'Bulkmeter',
        key: 'assets_bulkmeter',
        assetType: 'point',
    },
    {
        visible: true,
        label: 'Connectionmeter',
        key: 'assets_connectionmeter',
        assetType: 'point',
    },
    {
        visible: true,
        label: 'Consumptionmeter',
        key: 'assets_consumptionmeter',
        assetType: 'point',
    },
    {
        visible: true,
        label: 'IsolationValve',
        key: 'assets_isolationvalve',
        assetType: 'point',
    },
    {
        visible: true,
        label: 'Listeningpost',
        key: 'assets_listeningpost',
        assetType: 'point',
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
        visible: true,
        label: 'Pipes',
        key: 'assets_pipemain',
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

const AssetsBulkMeterColormap = {
    property: 'gid',
    colors: {
        Null: [220, 215, 71],
    },
    default: [144, 182, 111, 1],
};

const AssetsConnectionMeterColormap = {
    property: 'gid',
    colors: {
        Null: [220, 215, 71],
    },
    default: [236, 236, 41, 1],
};

const AssetsConsumptionMeterColormap = {
    property: 'gid',
    colors: {
        Null: [220, 215, 71],
    },
    default: [171, 234, 241, 1],
};

const AssetsIsolationValveColormap = {
    property: 'gid',
    colors: {
        Null: [220, 215, 71],
    },
    default: [210, 244, 39, 1],
};

const AssetsListeningPostColormap = {
    property: 'gid',
    colors: {
        Null: [220, 215, 71],
    },
    default: [220, 128, 238, 1],
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

function AssetsPressurefittingFillcolor(feature) {
    return getFillColorFeatures(feature, AssetsPressurefittingColormap);
}

function AssetsChamberFillcolor(feature) {
    return getFillColorFeatures(feature, AssetsChamberColormap);
}

function AssetsBulkMeterFillcolor(feature) {
    return getFillColorFeatures(feature, AssetsBulkMeterColormap);
}

function AssetsConnectionMeterFillcolor(feature) {
    return getFillColorFeatures(feature, AssetsConnectionMeterColormap);
}

function AssetsConsumptionMeterFillcolor(feature) {
    return getFillColorFeatures(feature, AssetsConsumptionMeterColormap);
}
function AssetsIsolationValveFillcolor(feature) {
    return getFillColorFeatures(feature, AssetsIsolationValveColormap);
}

function AssetsListeningPostFillcolor(feature) {
    return getFillColorFeatures(feature, AssetsListeningPostColormap);
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
    stroked: true,
};

async function getValues() {
    try {
        const url = `${GEOSERVER_URL}/geoserver/wfs?service=wfs&version=2.0.0&request=GetPropertyValue&typeNames=udt:utilities_dma&valueReference=code`;
        const username = 'admin';
        const password = `${GEOSERVER_ADMIN_PASSWORD}`;
        const credentials = `${username}:${password}`;
        const encodedCredentials = btoa(credentials);

        const headers = {
            'Authorization': `Basic ${encodedCredentials}`
        };

        const response = await fetch(url, { headers });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const xmlString = await response.text();
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(xmlString, 'application/xml');

        // Check for parse errors
        const parseError = xmlDoc.getElementsByTagName('parsererror');
        if (parseError.length > 0) {
            throw new Error(`Error parsing XML: ${parseError[0].textContent}`);
        }
        const evaluator = new XPathEvaluator();

        // Define namespace resolver
        const nsResolver = function(prefix) {
            const ns = {
                'wfs': 'http://www.opengis.net/wfs/2.0',
                'udt': 'http://udt'
            };
            return ns[prefix] || null;
        };

        const result = evaluator.evaluate('//wfs:member//udt:code', xmlDoc, nsResolver, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
        const values = [];
        for (let i = 0; i < result.snapshotLength; i++) {
            values.push(result.snapshotItem(i).textContent.trim());
        }
        return values;
    } catch (error) {
        // Log any errors that occur during the fetch or parsing
        console.error(error);
    }
}

async function getMapValues() {
    let MapValues = [];

    if (MapValues.length === 0) {
        const values = await getValues();
        MapValues = values;
    }

    return MapValues;
}

const DmaCodes = getMapValues();
//console.log(DmaCodes);
export const POINT_STYLING = (AssetName: string) => {
    let Styling = '';
    if (AssetName === 'assets_pressurefitting') {
        Styling = AssetsPressurefittingFillcolor;
    } else if (AssetName === 'assets_chamber') {
        Styling = AssetsChamberFillcolor;
    } else if (AssetName === 'assets_bulkmeter') {
        Styling = AssetsBulkMeterFillcolor;
    } else if (AssetName === 'assets_connectionmeter') {
        Styling = AssetsConnectionMeterFillcolor;
    } else if (AssetName === 'assets_consumptionmeter') {
        Styling = AssetsConsumptionMeterFillcolor;
    } else if (AssetName === 'assets_isolationvalve') {
        Styling = AssetsIsolationValveFillcolor;
    } else if (AssetName === 'assets_listeningpost') {
        Styling = AssetsListeningPostFillcolor;
    } else if (AssetName === 'assets_operationalsite') {
        Styling = AssetsOperationalsiteFillcolor;
    } else if (AssetName === 'assets_pressurecontrolvalve') {
        Styling = AssetsPressureControlValveFillcolor;
    }
    let StylingOptions;
    if (
        AssetName === 'assets_pressurefitting' ||
        AssetName === 'assets_chamber' ||
        AssetName === 'assets_operationalsite' ||
        AssetName === 'assets_pressurecontrolvalve' ||
        AssetName === 'assets_bulkmeter' ||
        AssetName === 'assets_connectionmeter' ||
        AssetName === 'assets_consumptionmeter' ||
        AssetName === 'assets_isolationvalve' ||
        AssetName === 'assets_listeningpost'
    ) {
        StylingOptions = {
            ...COMMON_STYLING,
            pointAntialiasing: true,
            radiusMinPixels: 8,
            radiusMaxPixels: 10,
            getPointRadius: 15,
            getFillColor: (f) => Styling(f),
        };
    }
    return StylingOptions;
};

export const LINE_STYLING = (AssetName: string) => {
    let ColorValue: number[] = [];
    if (AssetName === 'assets_pipemain') {
        ColorValue = [255, 96, 17];
    }

    return {
        ...COMMON_STYLING,
        getLineColor: ColorValue,
        lineWidthMinPixels: 1.5,
        lineWidthUnits: 'meters',
        lineCapRounded: true,
        lineJointRounded: true,
    };
};

export const POLYGON_STYLING = {
    ...COMMON_STYLING,
    opacity: 0.1,
    getFillColor: colorCategories({
        attr: 'code',
        domain: ['ZABINB01', 'ZABIND03', 'ZCHIPO01', 'ZABIND08'], // TODO: We need to call getValues(); to get the array
        colors: 'BluYl',
        othersColor: [72, 123, 182],
    }),
};
const assets_networkmeter_getIcon = (subtypes) => {
    switch (subtypes.subtype) {
        case 'distribution_input_meter':
            return 'network-meter-distribution-input-meter';
        case 'district_meter':
            return 'marker';
        case 'fire_meter':
            return 'network-meter-fire';
        case 'unknown':
            return 'network-meter-unknown';
        case 'waste_meter':
            return 'network-meter-waste';
        case 'zonal_meter':
            return 'network-meter-zonal';
        default:
            return 'network-meter-default';
    }
};

const assets_networkoptvalve_getIcon = (subtypes) => {
    switch (subtypes.gid) {
        default:
            return 'assets_networkoptvalve';
    }
};

const assets_logger_getIcon = (subtypes) => {
    switch (subtypes.gid) {
        default:
            return 'logger';
    }
};

const assets_hydrant_getIcon = (subtypes) => {
    switch (subtypes.gid) {
        default:
            return 'hydrant';
    }
};

const iconFunctions = {
    assets_networkmeter: (subtype) => assets_networkmeter_getIcon(subtype),
    assets_networkoptvalve: (subtype) =>
        assets_networkoptvalve_getIcon(subtype),
    assets_logger: (subtype) => assets_logger_getIcon(subtype),
    assets_hydrant: (subtype) => assets_hydrant_getIcon(subtype),
};

export const createLayers = (newMapLayerProps = []) => {
    const mapLayerProps = !_isEmpty(newMapLayerProps)? newMapLayerProps: MAP_LAYERS_PROPS;

    return _map(mapLayerProps, (layerProps) => {
        let LayerStyle = COMMON_STYLING;
        if (layerProps.assetType === 'point') {
            LayerStyle = POINT_STYLING(layerProps.key);
        } else if (layerProps.assetType === 'line') {
            LayerStyle = LINE_STYLING(layerProps.key);
        } else if (layerProps.assetType === 'polygon') {
            LayerStyle = POLYGON_STYLING;
        }
        if (
            layerProps.key === 'assets_hydrant' ||
            layerProps.key === 'assets_logger' ||
            layerProps.key === 'assets_networkoptvalve' ||
            layerProps.key === 'assets_networkmeter'
        ) {
            return new MVTLayer({
                pickable: true,
                id: layerProps.key,
                data: [MVT_LAYER_URL(layerProps.key)],
                visible: layerProps.visible,
                binary: false,
                minZoom: 13,
                maxZoom: 18,
                renderSubLayers: (props) => {
                    return new IconLayer(props, {
                        iconMapping:
                            'http://localhost:8080/geoserver/styles/sprites/makisprite.json',
                        iconAtlas:
                            'http://localhost:8080/geoserver/styles/sprites/makisprite.png',

                        getIcon: (f) => iconFunctions[layerProps.key](f.properties),
                        sizeMinPixels: 10,
                        sizeMaxPixels: 20,
                        sizeScale: 10,
                        sizeUnits: 'meters',
                        getPosition: (f) => f.geometry.coordinates,
                    });
                },
            });
        } else {
            return new MVTLayer({
                pickable: true,
                id: layerProps.key,
                data: [MVT_LAYER_URL(layerProps.key)],
                visible: layerProps.visible,
                ...LayerStyle,
            });
        }
    });
};
