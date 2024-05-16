import { createContext, Dispatch, SetStateAction } from 'react';
import { MapViewState } from '@deck.gl/core';

export type MapContextType = {
    initialView: MapViewState;
    setInitialView: Dispatch<SetStateAction<MapViewState>>;
    showLayerToggle: boolean;
    setShowLayerToggle: Dispatch<SetStateAction<boolean>>;
    showBaseMapToggle: boolean;
    setShowBaseMapToggle: Dispatch<SetStateAction<boolean>>;
}

export const MapContext = createContext<MapContextType>({
    initialView: {
        longitude: 0,
        latitude: 0,
        zoom: 0,
        bearing: 0,
        pitch: 0,
    },
    setInitialView: () => {},
    // gotoLocation: {},
    // setGotoLocation: () => {},
    showLayerToggle: false,
    setShowLayerToggle: () => {},
    showBaseMapToggle: false,
    setShowBaseMapToggle: () => {},
});
