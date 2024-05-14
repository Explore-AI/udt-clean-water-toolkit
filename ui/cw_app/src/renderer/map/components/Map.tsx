// Our Map Page details exists here
import DeckGL from '@deck.gl/react';

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
    LAYER_NAME_COLOR_CODES,
    DEFAULT_LAYER_TOGGLE,
    DEFAULT_BASEMAP_TOGGLE,
} from '../../core';
import GeoSpatialControls from './MapControl';
import * as styles from '../css/Map.module.css';
import { useState, useContext } from 'react';
import { MapContext } from '../context/MapContext';
import ToggleViewPopup from './TogglePopup';
import { LayerToggleObject, BasemapToggleObject, LayerToggle, BasemapToggle } from '../types/types';

if (!MAPBOX_TOKEN) {
    throw new Error('Missing Mapbox token');
}

// const INITIAL_VIEW_STATE: MapViewState = {
//     longitude: -0.118092,
//     latitude: 51.5074,
//     zoom: 10,
//     bearing: 0,
//     pitch: 30,
// };

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
    const { initialView, showBaseMapToggle, showLayerToggle } =
        useContext(MapContext);
    const [toggleLayers, setToggleLayers] =
        useState<LayerToggle[]>(DEFAULT_LAYER_TOGGLE);
    const [toggleBaseMap, setToggleBaseMap] = useState<BasemapToggle[]>(
        DEFAULT_BASEMAP_TOGGLE,
    );
    console.log(`Your Toggling Layers: ${toggleLayers}`);
    console.log(`Your Toggling BaseMap: ${toggleBaseMap}`);
    return (
        <>
            <div className={styles.searchBox}>
                <SearchWidget />
            </div>
            <div className={styles.control}>
                <GeoSpatialControls />
            </div>
            {showLayerToggle && (
                <div className={styles.layerTogglePopup}>
                    <ToggleViewPopup toggleList={toggleLayers} />
                </div>
            )}
            {/* {
                showBaseMapToggle && 
                <div className={styles.basemapTogglePopup} > 
                    <ToggleViewPopup message='Basemap Toggle' />
                </div>
            } */}

            <DeckGL
                initialViewState={initialView}
                controller={{ scrollZoom: true }}
                // layers={layers}
            >
                <Map
                    initialViewState={initialView}
                    mapStyle={BASEMAP.POSITRON}
                    mapboxAccessToken={MAPBOX_TOKEN}
                    style={{ width: '500px', height: '500px' }}
                    attributionControl={false}
                />
            </DeckGL>
        </>
    );
}
