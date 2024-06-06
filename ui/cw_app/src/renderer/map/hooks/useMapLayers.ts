import { createContext, useState, useEffect } from 'react';
import { createLayers, DEFAULT_BASEMAP_PROPS, MAP_LAYERS_PROPS } from '../utils/mapUtils';

import { unionBy as _unionBy } from 'lodash';

export const MapLayerContext = createContext();

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
