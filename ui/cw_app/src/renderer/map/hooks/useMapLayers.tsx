import React, { useContext, useState, useEffect } from 'react';
import { MAP_LAYERS_INFO, MVT_LAYER_URL } from '../../core';
import { MVTLayer } from '@deck.gl/geo-layers';

const MVT_LAYERS = MAP_LAYERS_INFO.map((layer: MAP_LAYERS_INFO) => {
    console.log(layer)
    return new MVTLayer({
        id: layer.key,
        data: [MVT_LAYER_URL(layer.key)],
        pickable: true,
        getFillColor: layer.colorCode,
        getPointRadius: 10,
        visible: layer.visible,
        minZoom: 0,
        maxZoom: 5,
    });
});

export default function useMapLayers(mapLayerVisibility = {}) {
    //const [mapLayerVisibility, setMapLayerVisibility] = useState({});
    const [mapLayers, setMapLayers] = useState(MVT_LAYERS);
    console.log(mapLayers, "qqqqqqqq")
    /* const handleMapLayerVisibility = (newParams, options = {}) => {
     *     map();
     *     return mapLayerVisibility;
     * }; */

    useEffect(() => {
        const layers = mapLayers.map(() => null)

        return () => {};
    }, []);

    return { mapLayers: MVT_LAYERS };
}
