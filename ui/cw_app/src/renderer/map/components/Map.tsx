// Our Map Page details exists here
import DeckGL from '@deck.gl/react';
import * as styles from '../css/Map.module.css';
import SearchWidget from '../../core/components/SearchWidget';
import BaseLayout from '../../core/components/BaseLayout';
import { MapViewState } from '@deck.gl/core';
import { Map } from 'react-map-gl';
import { BASEMAP } from '@deck.gl/carto';
import { MAPBOX_TOKEN } from '../../config';
import { MVTLayer } from '@deck.gl/geo-layers';
import {
    LAYER_NAMES,
    MVT_LAYER_URL,
    LAYER_NAME_COLOR_CODES
} from '../../core';

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

// const layers = Object.entries(LAYER_NAMES).map(([key, value]) => {
//     return new MVTLayer({
//         id: key,
//         data: [MVT_LAYER_URL(value)],
//         pickable: true,
//         //@ts-ignore
//         getFillColor: LAYER_NAME_COLOR_CODES[key],
//         getPointRadius: 10,
//         minZoom: 0,
//         maxZoom: 5,
//     });
// })

export default function MapPage() {

    return (
      <>
        <div className={styles.searchBox}>
          <SearchWidget />
        </div>
        <DeckGL
          initialViewState={INITIAL_VIEW_STATE}
          controller={{ scrollZoom: true }}
          // layers={layers}
          >
          <Map
            initialViewState={INITIAL_VIEW_STATE}
            mapStyle={BASEMAP.POSITRON}
            mapboxAccessToken={MAPBOX_TOKEN}
            style={{ width: '500px', height: '500px' }}
          />
        </DeckGL>
      </>
    );
}
