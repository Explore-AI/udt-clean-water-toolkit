import React, { useContext } from 'react';
import { MapContext } from '../context/MapContext';
import { MapViewState } from 'deck.gl';

export const useMapContext = () => {
    const context = useContext(MapContext);
    if (!context) {
        throw new Error('useMapContext must be used within a MapProvider');
    }
    return context;
};

export const useInitialView = (): [
    MapViewState,
    React.Dispatch<React.SetStateAction<MapViewState>>,
] => {
    const { initialView, setInitialView } = useMapContext();
    return [initialView, setInitialView];
};

export const useLayerToggle = (): [
    boolean,
    React.Dispatch<React.SetStateAction<boolean>>,
] => {
    const { showLayerToggle, setShowLayerToggle } = useMapContext();
    return [showLayerToggle, setShowLayerToggle];
};

export const useBasemapToggle = (): [
    boolean,
    React.Dispatch<React.SetStateAction<boolean>>,
] => {
    const { showBaseMapToggle, setShowBaseMapToggle } = useMapContext();
    return [showBaseMapToggle, setShowBaseMapToggle];
};

export const useGoToLocation = (): [
    { latitude: number; longitude: number },
    React.Dispatch<
        React.SetStateAction<{ latitude: number; longitude: number }>
    >,
] => {
    const { gotoLocation, setGotoLocation } = useMapContext();
    return [gotoLocation, setGotoLocation];
};
