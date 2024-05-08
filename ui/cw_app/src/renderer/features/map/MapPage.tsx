// Our Map Page details exists here
import DeckGL from '@deck.gl/react';
import { MapViewState } from '@deck.gl/core';


const INITIAL_VIEW_STATE: MapViewState = {
    longitude: -122.4,
    latitude: 37.8,
    zoom: 15,
    bearing: 0,
    pitch: 30,
};

export default function MapPage() {
    return (
        <div style={{ border: '1px solid black' }}>
            <DeckGL
                initialViewState={INITIAL_VIEW_STATE}
                controller={{ scrollZoom: true }}
            >
            </DeckGL>
        </div>
    );
}
