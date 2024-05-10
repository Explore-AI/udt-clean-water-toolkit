// Our Map Page details exists here
import 'dotenv';
import DeckGL from '@deck.gl/react';
import { MapViewState } from '@deck.gl/core';
import { Map } from 'react-map-gl';
import { BASEMAP } from '@deck.gl/carto';
import styles from '../css/MapPage.module.css';
import SearchWidget from '../../core/SearchWidget';
import BaseLayout from '../../core/components/BaseLayout';
import {
    MAPBOX_TOKEN,
    LAYER_NAMES,
    MVT_LAYER_URL,
    LAYER_NAME_COLOR_CODES
} from '../../core/constants';
import { MVTLayer } from '@deck.gl/geo-layers';


if (!MAPBOX_TOKEN) {
    throw new Error('Missing Mapbox token');
}

// Define the structure of the tooltip
const INITIAL_VIEW_STATE: MapViewState = {
    longitude: -0.118092,
    latitude: 51.5074,
    zoom: 10,
    bearing: 0,
    pitch: 30,
};

export default function MapPage() {
    const layers = Object.entries(LAYER_NAMES).map(([key, value]) => {
        return new MVTLayer({
            id: key,
            data: [MVT_LAYER_URL(value)],
            pickable: true,
            //@ts-ignore
            getFillColor: LAYER_NAME_COLOR_CODES[key],
            getPointRadius: 10,
            minZoom: 0,
            maxZoom: 5,
        });
    })

    return (
        <BaseLayout>
            <div className={styles['page-container']}>
                <SearchWidget />
                <DeckGL
                    initialViewState={INITIAL_VIEW_STATE}
                    controller={{ scrollZoom: true }}
                    layers={layers}
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
