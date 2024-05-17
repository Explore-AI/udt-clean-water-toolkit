// Our Map Page details exists here
import DeckGL from '@deck.gl/react';
import SearchWidget from '../../core/components/SearchWidget';
import { Map } from 'react-map-gl';
import { MAPBOX_SECRET_TOKEN, MAPBOX_PUBLIC_TOKEN } from '../../config';
import { MVTLayer } from '@deck.gl/geo-layers';
import {
    MVT_LAYER_URL,
    LAYER_NAME_COLOR_CODES,
    DEFAULT_LAYER_TOGGLE,
    DEFAULT_BASEMAP_TOGGLE,
} from '../../core';
import GeoSpatialControls from './MapControl';
import styles from '../css/Map.module.css';
import { useState } from 'react';
import { useLayerToggle, useBasemapToggle } from '../hooks/useMapContext';
import BasePopup from '../../core/components/BasePopup';
import RadioButtonList from './RadioButtonList';
import CheckboxList from './CheckBoxList';
import { LayerToggle, BasemapToggle } from '../types/types';
import { INITIAL_VIEW_STATE } from '../../core';
import { MapViewState } from 'deck.gl';
import useMapUi from '../hooks/useMapUi'



if (!MAPBOX_SECRET_TOKEN) {
    throw new Error('Missing Mapbox token');
}

const getLayers = (layerList: LayerToggle[]) => {
    return layerList
        .filter((layer: LayerToggle) => layer.visible)
        .map((layer: LayerToggle) => {
            return new MVTLayer({
                id: layer.key,
                data: [MVT_LAYER_URL(layer.key)],
                pickable: true,
                //@ts-ignore
                getFillColor: LAYER_NAME_COLOR_CODES[layer.key],
                getPointRadius: 10,
                minZoom: 0,
                maxZoom: 5,
            });
        });
};

const basemapUrl = (basemapList: BasemapToggle[]) => {
    return basemapList.find((toggle: BasemapToggle) => toggle.visible)?.map_url;
};

export default function MapView() {

    //const [initialView, setInitialView] = useState<MapViewState>(INITIAL_VIEW_STATE);

    const [toggleLayers, setToggleLayers] =
        useState<LayerToggle[]>(DEFAULT_LAYER_TOGGLE);

    const [toggleBaseMap, setToggleBaseMap] = useState<BasemapToggle[]>(
        DEFAULT_BASEMAP_TOGGLE,
    );

    const { showLayerToggle, showBaseMapToggle } = useMapUi

    const currentBaseMapUrl = basemapUrl(toggleBaseMap);
    const layers = getLayers(toggleLayers);

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
                    <BasePopup>
                        <CheckboxList
                            toggleList={toggleLayers}
                            setToggleList={setToggleLayers}
                        />
                    </BasePopup>
                </div>
            )}

            {showBaseMapToggle && (
                <div className={styles.basemapTogglePopup}>
                    <BasePopup>
                        <RadioButtonList
                            toggleList={toggleBaseMap}
                            setToggleList={setToggleBaseMap}
                        />
                    </BasePopup>
                </div>
            )}

            <DeckGL
                initialViewState={INITIAL_VIEW_STATE}
                controller={{ scrollZoom: true }}
                layers={layers}
            >
                <Map
                    initialViewState={INITIAL_VIEW_STATE}
                    mapStyle={currentBaseMapUrl}
                    mapboxAccessToken={MAPBOX_PUBLIC_TOKEN}
                    style={{ width: '500px', height: '500px' }}
                    attributionControl={false}
                />
            </DeckGL>
        </>
    );
}
