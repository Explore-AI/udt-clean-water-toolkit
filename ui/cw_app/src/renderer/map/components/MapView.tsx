// Our Map Page details exists here
import DeckGL from '@deck.gl/react';
import SearchWidget from '../../core/components/SearchWidget';
import { Map } from 'react-map-gl';
import { MAPBOX_SECRET_TOKEN, MAPBOX_PUBLIC_TOKEN } from '../../config';
import { DEFAULT_BASEMAP_TOGGLE } from '../../core';
import { MVTLayer } from '@deck.gl/geo-layers';
import MapControls from './MapControls';
import styles from '../css/Map.module.css';
import { useState } from 'react';
import { useLayerToggle, useBasemapToggle } from '../hooks/useMapContext';
import BasePopup from '../../core/components/BasePopup';
import RadioButtonList from './RadioButtonList';
import CheckboxList from './CheckBoxList';
import { LayerToggle, BasemapToggle } from '../types/types';
import { MapViewState } from 'deck.gl';
import useMapUi from '../hooks/useMapUi';
import useMapLayers from '../hooks/useMapLayers';

if (!MAPBOX_SECRET_TOKEN) {
    throw new Error('Missing Mapbox token');
}

export const INITIAL_VIEW_STATE: MapViewState = {
    longitude: -0.118092,
    latitude: 51.5074,
    zoom: 10,
    bearing: 0,
    pitch: 30,
};

export default function MapView() {
    const { mapLayers } = useMapLayers();
    console.log(mapLayers, 'eeeeeeeee');

    return (
        <>
            {/* <div className={styles.searchBox}>
                <SearchWidget />
                </div>
                <div className={styles.control}>
                <MapControls />
                </div> */}
            <DeckGL
                initialViewState={INITIAL_VIEW_STATE}
                controller={{ scrollZoom: true }}
                layers={mapLayers}
            >
                <Map
                    initialViewState={INITIAL_VIEW_STATE}
                    mapStyle={DEFAULT_BASEMAP_TOGGLE[0].map_url}
                    mapboxAccessToken={MAPBOX_PUBLIC_TOKEN}
                    style={{ width: '500px', height: '500px' }}
                    attributionControl={false}
                />
            </DeckGL>
        </>
    );
}
