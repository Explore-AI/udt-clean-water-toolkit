import React, { useState } from 'react';
import { MapContext, MapContextType } from './MapContext';
import { MapViewState } from 'deck.gl';
import { INITIAL_VIEW_STATE, INITIAL_COORDS } from '../../core';

type MapProviderProps = {
    children: React.ReactNode;
};

function MapContextProvider({ children }: MapProviderProps) {
    const [initialView, setInitialView] =
        useState<MapViewState>(INITIAL_VIEW_STATE);
    const [gotoLocation, setGotoLocation] = useState(INITIAL_COORDS);
    const [showLayerToggle, setShowLayerToggle] = useState(false);
    const [showBaseMapToggle, setShowBaseMapToggle] = useState(false);

    const contextValues: MapContextType = {
        initialView,
        setInitialView,
        gotoLocation,
        setGotoLocation,
        showLayerToggle,
        setShowLayerToggle,
        showBaseMapToggle,
        setShowBaseMapToggle,
    };

    return (
        <MapContext.Provider value={contextValues}>
            {children}
        </MapContext.Provider>
    );
}

export default MapContextProvider;
