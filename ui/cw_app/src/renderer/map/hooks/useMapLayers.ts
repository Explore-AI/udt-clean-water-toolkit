import { createContext, useState, useEffect } from 'react';
import { createLayers, DEFAULT_BASEMAP_PROPS, MAP_LAYERS_PROPS } from '../utils/mapUtils';

import { map as _map } from 'lodash';

export const MapLayerContext = createContext();

export default function useMapLayers() {
    const [baseMap, setBaseMap] = useState(DEFAULT_BASEMAP_PROPS[0]);

    const [mapLayerProps, setMapLayerProps] = useState(MAP_LAYERS_PROPS);
    const [mapLayers, setMapLayers] = useState(createLayers());

    const handleMapLayerProps = (newLayerProps) => {
        const newMapLayerProps = _map(
            mapLayerProps,
            (layerProp) => {
                if (layerProp.key == newLayerProps.key) {
                    return {...layerProp, ...newLayerProps}
                }
                return layerProp
            }
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
