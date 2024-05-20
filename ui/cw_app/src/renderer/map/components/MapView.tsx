// Our Map Page details exists here
import styles from '../css/Map.module.css';
import DeckGL from '@deck.gl/react';
import SearchWidget from '../../core/components/SearchWidget';
import MapControls from './MapControls';
import useMapUi from '../hooks/useMapUi';
import useMapLayers from '../hooks/useMapLayers';
import { Map } from 'react-map-gl';
import { MapViewState } from 'deck.gl';
import { MAPBOX_PUBLIC_TOKEN } from '../../config';
import { DEFAULT_BASEMAP_PROPS } from '../../core';

export const INITIAL_VIEW_STATE: MapViewState = {
    longitude: -0.118092,
    latitude: 51.5074,
    zoom: 10,
    bearing: 0,
    pitch: 30,
};

export default function MapView() {
    const { mapLayers } = useMapLayers();

    return (
        <>
            <div className={styles.control}>
                <MapControls />
            </div>
            <DeckGL
                initialViewState={INITIAL_VIEW_STATE}
                controller={{ scrollZoom: true }}
                layers={mapLayers}
            >
                <Map
                    initialViewState={INITIAL_VIEW_STATE}
                    mapStyle={DEFAULT_BASEMAP_PROPS[0].map_url}
                    mapboxAccessToken={MAPBOX_PUBLIC_TOKEN}
                    style={{ width: '500px', height: '500px' }}
                    attributionControl={false}
                />
            </DeckGL>
        </>
    );
}

// <div className={styles.searchBox}>
//         <SearchWidget />
//         </div>
