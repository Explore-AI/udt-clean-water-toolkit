import { createContext, useState, useEffect } from 'react';
import {
    MAP_LAYERS_PROPS,
    MVT_LAYER_URL,
    MVT_LAYER_URL_TWO,
    DEFAULT_BASEMAP_PROPS,
} from '../../core';
import { MVTLayer } from '@deck.gl/geo-layers';
import { map as _map, unionBy as _unionBy, isEqual as _isEqual, isEmpty as _isEmpty } from 'lodash';

export const MapLayerContext = createContext();

const createLayers = (newMapLayerProps = []) => {
    const mapLayerProps = !_isEmpty(newMapLayerProps)? newMapLayerProps: MAP_LAYERS_PROPS;

    return _map(mapLayerProps, (layerProps) => {
        return new MVTLayer({
            pickable: true,
            // scheme: 'tms',
            id: layerProps.key,
            visible: layerProps.visible,
            lineWidthMinPixels: 1,
            getLineColor: layerProps.colorCode,
            getLineCap: 'round',
            data: [MVT_LAYER_URL(layerProps.key)],
            getFillColor: layerProps.colorCode,
            opacity: layerProps.opacity
        });
    });
};

export default function useMapLayers() {
    const [baseMap, setBaseMap] = useState(DEFAULT_BASEMAP_PROPS[0]);

    const [mapLayerProps, setMapLayerProps] = useState(MAP_LAYERS_PROPS);
    const [mapLayers, setMapLayers] = useState(createLayers());

    const handleMapLayerProps = (newLayerProps) => {
        const newMapLayerProps = _unionBy(
            mapLayerProps,
            [newLayerProps],
            'key',
        );

        setMapLayerProps(newMapLayerProps);

        const layers = createLayers(newMapLayerProps);
        setMapLayers(layers);
    };

    return {
        mapLayerProps,
        setMapLayerProps: handleMapLayerProps,
        mapLayers,
        baseMap,
        setBaseMap,
    };
}
