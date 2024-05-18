import React, { useContext, useState } from 'react';
import { MAP_LAYERS_INFO } from '../../core';

const MVT_LAYERS = map((layer: MAP_LAYERS_INFO) => {
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

export default function useMapLayers() {
    const [uiParams, setMapUiParams] = useState({});

    const handleMapUiParams = (newParams, options = {}) => {
        if (isEmpty(newParams) || isNil(newParams)) {
            return setMapUiParams({});
        }
        return setUiParams({ ...uiParams, ...newParams });
    };

    return { uiParams, setMapUiParams: handleMapUiParams };
}
