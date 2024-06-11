import { MapViewState } from '@deck.gl/core';
import { MVTLayer } from '@deck.gl/geo-layers';
import { IconLayer } from '@deck.gl/layers';
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

function AssetsHydrantFillcolor() {
    return {
        binary: false,
        minZoom: 8,
        maxZoom: 18,
        renderSubLayers: props => {
            return new IconLayer(props, {
                iconMapping:
                    'https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/icon-atlas.json',
                iconAtlas: `${GEOSERVER_URL}/geoserver/styles/sprites/makisprite.png`,
                getIcon: (f: Feature<Geometry, PropertiesType>) => {
                    switch (f.properties.gid) {
                        case 'x':
                            return 'hydrant';
                        default:
                            return 'hydrant';
                    }
                },
                sizeScale: 1.5,
                getSize: 10,
                getColor: [234, 122, 100],
                getPosition: (f) => f.geometry.coordinates,
            });
        },
    };
}

function AssetsLoggerFillcolor() {
    return {
        binary: false,
        minZoom: 8,
        maxZoom: 18,
        renderSubLayers: props => {
            return new IconLayer(props, {
                iconMapping:
                    'https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/icon-atlas.json',
                iconAtlas: `${GEOSERVER_URL}/geoserver/styles/sprites/makisprite.png`,
                getIcon: (f: Feature<Geometry, PropertiesType>) => {
                    switch (f.properties.gid) {
                        case 'x':
                            return 'logger';
                        default:
                            return 'logger';
                    }
                },
                sizeScale: 1.5,
                getSize: 10,
                getColor: [234, 122, 100],
                getPosition: (f) => f.geometry.coordinates,
            });
        },
    };
}
function AssetsNetworkmeterFillcolor() {
    return {
        binary: false,
        minZoom: 8,
        maxZoom: 18,
        renderSubLayers: props => {
            return new IconLayer(props, {
                iconMapping:
                    'https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/icon-atlas.json',
                iconAtlas: `${GEOSERVER_URL}/geoserver/styles/sprites/makisprite.png`,
                getIcon: (f: Feature<Geometry, PropertiesType>) => {
                    switch (f.properties.subtype) {
                        case 'distribution_input_meter':
                            return 'network-meter-distribution-input-meter';
                        case 'district_meter':
                            return 'network-meter-distribution-input-meter';
                        case 'fire_meter':
                            return 'network-meter-fire';
                        case 'unknown':
                            return 'network-meter-unkown';
                        case 'waste_meter':
                            return 'network-meter-waste';
                        case 'zonal_meter':
                            return 'network-meter-zonal';
                        default:
                            return 'assets_networkoptvalve';
                    }
                },
                sizeScale: 1.5,
                getSize: 10,
                getColor: [234, 122, 100],
                getPosition: (f) => f.geometry.coordinates,
            });
        },
    };
}

function AssetsNetworkoptvalveFillcolor() {
    return {
        binary: false,
        minZoom: 8,
        maxZoom: 18,
        renderSubLayers: props => {
            return new IconLayer(props, {
                iconMapping:
                    'https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/icon-atlas.json',
                iconAtlas: `${GEOSERVER_URL}/geoserver/styles/sprites/makisprite.png`,
                getIcon: (f: Feature<Geometry, PropertiesType>) => {
                    switch (f.properties.gid) {
                        case 'x':
                            return 'assets_networkoptvalve';
                        default:
                            return 'assets_networkoptvalve';
                    }
                },
                sizeScale: 1.5,
                getSize: 10,
                getColor: [234, 122, 100],
                getPosition: (f) => f.geometry.coordinates,
            });
        },
    };
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

export const POINT_STYLING = (AssetName: string) => {
    let Styling = '';
    if (AssetName === 'assets_pressurefitting') {
        Styling = AssetsPressurefittingFillcolor;
    } else if (AssetName === 'assets_chamber') {
        Styling = AssetsChamberFillcolor;
    } else if (AssetName === 'assets_hydrant') {
        Styling = AssetsHydrantFillcolor();
    } else if (AssetName === 'assets_logger') {
        Styling = AssetsLoggerFillcolor();
    } else if (AssetName === 'assets_networkmeter') {
        Styling = AssetsNetworkmeterFillcolor();
    } else if (AssetName === 'assets_networkoptvalve') {
        Styling = AssetsNetworkoptvalveFillcolor();
    } else if (AssetName === 'assets_operationalsite') {
        Styling = AssetsOperationalsiteFillcolor;
    } else if (AssetName === 'assets_pressurecontrolvalve') {
        Styling = AssetsPressureControlValveFillcolor;
    }
    let StylingOptions;
    if (
        AssetName === 'assets_hydrant' ||
        AssetName === 'assets_logger' ||
        AssetName === 'assets_networkoptvalve' ||
        AssetName === 'assets_networkmeter'
    ) {
        StylingOptions = Styling;
    } else {
        StylingOptions = {
            ...COMMON_STYLING,
            pointAntialiasing: true,
            radiusMinPixels: 20,
            radiusMaxPixels: 10,
            getPointRadius: 40,
            getFillColor: (f) => Styling(f),
        };
    }
    return StylingOptions;
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
        domain: ['ZABINB01', 'ZABIND03', 'ZCHIPO01', 'ZABIND08'], // TODO: get dmas from from geoserver
        colors: 'BluYl',
        othersColor: [72, 123, 182],
    }),
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
        return new MVTLayer({
            pickable: true,
            id: layerProps.key,
            data: [MVT_LAYER_URL(layerProps.key)],
            visible: layerProps.visible,
            ...LayerStyle,
        });
    });
};
