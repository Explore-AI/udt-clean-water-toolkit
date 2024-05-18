import React, { useContext, useState } from 'react';

export const MAP_LAYERS = [
    {
        visible: false,
        label: 'Chambers',
        key: 'assets_chamber'
        color_code: [245, 183, 177]
    },
    {
        visible: false,
        label: 'Distribution Main',
        key: 'assets_distributionmain',
        color_code: [162, 217, 206]
    },
    {
        visible: false,
        label: 'Hydrants',
        key: 'assets_hydrant'
        color_code:[0, 158, 222],
    },
    {
        visible: false,
        label: 'Loggers',
        key: 'assets_logger'
    },
    {
        visible: false,
        label: 'Network Meter',
        key: 'assets_networkmeter'
    },
    {
        visible: false,
        label: 'Network Opt Valve',
        key: 'assets_networkoptvalve',
    },
    {
        visible: false,
        label: 'Operational Site',
        key: 'assets_operationalsite',
    },
    {
        visible: false,
        label: 'Pressure Control Valve',
        key: 'assets_pressurecontrolvalve',
    },
    {
        visible: false,
        label: 'Pressure Fitting',
        key: 'assets_pressurefitting',
    },
    {
        visible: false,
        label: 'Trunk Main',
        key: 'assets_trunkmain'
    },
];

const getLayers = (layerList: LayerToggle[]) => {
    return layerList
        .filter((layer: LayerToggle) => layer.visible)
        .map((layer: LayerToggle) => {
            return new MVTLayer({
                id: layer.key,
                data: [MVT_LAYER_URL(layer.key)],
                pickable: true,
                //@ts-ignore
                getFillColor: LAYER_NAME_COLOR_CODES[layer.key],
                getPointRadius: 10,
                minZoom: 0,
                maxZoom: 5,
            });
        });
};

export default function useMapUi() {

    const [showLayerToggle, setShowLayerToggle] = useState(false);
    const [showBaseMapToggle, setShowBaseMapToggle] = useState(false);

    //const values = useContext(MapUiContext);

    //    console.log(values, "aaa")

    const values = { showLayerToggle, showBaseMapToggle }

    console.log(values, "aaa")



    return values;
};
