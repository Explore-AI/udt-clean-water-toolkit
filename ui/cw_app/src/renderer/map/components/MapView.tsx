// Our Map Page details exists here
import styles from '../css/MapView.module.css';
import { useContext } from 'react';
import DeckGL from '@deck.gl/react';
import MapControls from './MapControls';
import MapSearchBox from '../components/MapSearchBox';
import { Map } from 'react-map-gl';
import { MapViewState } from 'deck.gl';
import { MAPBOX_PUBLIC_TOKEN } from '../../config';
import { useParams } from 'react-router-dom';
import { MapLayerContext } from '../hooks/useMapLayers';

const INITIAL_VIEW_STATE: MapViewState = {
    longitude: -0.118092,
    latitude: 51.5074,
    zoom: 10,
    bearing: 0,
    pitch: 30,
};

export default function MapView() {
    const { latlong } = useParams();
    const { mapLayers, baseMap } = useContext(MapLayerContext);

    console.log(latlong, 'ssss333');

    let viewState;
    if (latlong) {
        const latitude = latlong.split(',')[0];
        const longitude = latlong.split(',')[1];
        viewState = {
            ...INITIAL_VIEW_STATE,
            latitude: latitude,
            longitude: longitude,
        };
    } else {
        viewState = INITIAL_VIEW_STATE;
    }

    return (
        <>
            <div className={styles.searchBox}>
                <MapSearchBox />
            </div>
            <div className={styles.control}>
                <MapControls />
            </div>
            <DeckGL
                initialViewState={viewState}
                controller={{ scrollZoom: true }}
                layers={mapLayers}
            >
                <Map
                    initialViewState={viewState}
                    mapStyle={baseMap.mapUrl}
                    mapboxAccessToken={MAPBOX_PUBLIC_TOKEN}
                    style={{ width: '500px', height: '500px' }}
                    attributionControl={false}
                />
            </DeckGL>
        </>
    );
}
