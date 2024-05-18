import React, { useContext, useState } from 'react';

export const MapUiContext = React.createContext();

export default function useMapUi() {
    const [showLayerToggle, setShowLayerToggle] = useState(false);
    const [showBaseMapToggle, setShowBaseMapToggle] = useState(false);

    //const values = useContext(MapUiContext);

    //    console.log(values, "aaa")

    const values = { showLayerToggle, showBaseMapToggle };

    console.log(values, 'aaa');

    return values;
}
