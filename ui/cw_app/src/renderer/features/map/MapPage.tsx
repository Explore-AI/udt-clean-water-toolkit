// Our Map Page details exists here
import DeckGL from '@deck.gl/react';
import { MapViewState } from '@deck.gl/core';
import { Map } from 'react-map-gl';
// import StaticMap from 'react-map-gl';
import { BASEMAP } from '@deck.gl/carto';


const MAPBOX_TOKEN = "";
if (!MAPBOX_TOKEN) {
    throw new Error('Missing Mapbox token');
}

const INITIAL_VIEW_STATE: MapViewState = {
    longitude: -122.4,
    latitude: 37.8,
    zoom: 15,
    bearing: 0,
    pitch: 30,
};

export default function MapPage() {
    console.log(MAPBOX_TOKEN);
    return (
        <div style={{ border: '1px solid black' }}>
            <DeckGL
                initialViewState={INITIAL_VIEW_STATE}
                controller={{ scrollZoom: true }}
            >
                <Map
                    mapStyle={BASEMAP.DARK_MATTER}
                    mapboxAccessToken={MAPBOX_TOKEN}
                />
            </DeckGL>
        </div>
    );
}
