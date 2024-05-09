// Our Map Page details exists here
import 'dotenv';
import DeckGL from '@deck.gl/react';
import { MapViewState } from '@deck.gl/core';
import { Map } from 'react-map-gl';
import { BASEMAP } from '@deck.gl/carto';
import styles from '../css/MapPage.module.css';
import SearchWidget from '../../core/SearchWidget'
import BaseLayout from '../../core/components/BaseLayout'

const MAPBOX_TOKEN = process.env.MAPBOX_TOKEN;

if (!MAPBOX_TOKEN) {
    throw new Error('Missing Mapbox token');
}

const INITIAL_VIEW_STATE: MapViewState = {
    longitude: -0.118092,
    latitude: 51.5074,
    zoom: 10,
    bearing: 0,
    pitch: 30,
};

export default function MapPage() {
    return (
        <BaseLayout>
            <div
                className={styles['page-container']}
            >
                <SearchWidget />
                <DeckGL
                    initialViewState={INITIAL_VIEW_STATE}
                    controller={{ scrollZoom: true }}
                >
                    <Map
                        initialViewState={INITIAL_VIEW_STATE}
                        mapStyle={BASEMAP.POSITRON}
                        mapboxAccessToken={MAPBOX_TOKEN}
                        style={{ width: '500px', height: '500px' }}
                    />
                </DeckGL>
            </div>
        </BaseLayout>
    );
}
