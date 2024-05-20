import React, { useContext, useState, useEffect } from 'react';
import { MAP_LAYERS_PROPS, MVT_LAYER_URL, DEFAULT_BASEMAP_PROPS } from '../../core';
import { MVTLayer } from '@deck.gl/geo-layers';
import { map as _map, unionBy as _unionBy, isEqual as _isEqual } from 'lodash';

const createLayers = (newMapLayerProps = []) => {
    const mapLayerProps = newMapLayerProps || MAP_LAYERS_PROPS;

    return _map(mapLayerProps, (layerProps) => {
        return new MVTLayer({
            pickable: true,
            getPointRadius: 10,
            minZoom: 0,
            maxZoom: 5,
            id: layerProps.key,
            visible: layerProps.visible,
            getFillColor: layerProps.colorCode,
            data: [MVT_LAYER_URL(layerProps.key)],
        });
    });
};

export default function useMapLayers() {
    const [mapLayerProps, setMapLayerProps] = useState(MAP_LAYERS_PROPS);
    const [baseMapUrl, setBaseMapUrl] = useState(DEFAULT_BASEMAP_PROPS[0].map_url);
    console.log(baseMapUrl)
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
        console.log(layers);
    };

    return { mapLayerProps, setMapLayerProps: handleMapLayerProps, mapLayers, baseMapUrl, setBaseMapUrl };
}
