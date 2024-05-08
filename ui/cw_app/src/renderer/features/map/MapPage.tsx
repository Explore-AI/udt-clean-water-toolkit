// Our Map Page details exists here
import DeckGL from '@deck.gl/react';
import { MapViewState } from '@deck.gl/core';
import { Map } from 'react-map-gl';
// import StaticMap from 'react-map-gl';
import { BASEMAP } from '@deck.gl/carto';
import 'dotenv';

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
        <div
            style={{
                width: '99vw',
                height: '600px',
            }}
        >
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
    );
}
