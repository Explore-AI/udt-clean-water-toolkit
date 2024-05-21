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
import { useState, useEffect } from 'react';
import {
    useInitialView,
    useLayerToggle,
    useBasemapToggle,
    useGoToLocation,
} from '../hooks/useMapContext';
import BasePopup from '../../core/components/BasePopup';
import RadioButtonList from './RadioButtonList';
import CheckboxList from './CheckBoxList';
import { LayerToggle, BasemapToggle } from '../types/types';
import { isValidCoordinate } from '../../core/utils/utils';

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
    const [initialView, setInitialView] = useInitialView();
    const [showBaseMapToggle] = useBasemapToggle();
    const [showLayerToggle] = useLayerToggle();
    const [gotoLocation, setGotoLocation] = useGoToLocation();

    const [toggleLayers, setToggleLayers] =
        useState<LayerToggle[]>(DEFAULT_LAYER_TOGGLE);
    const [toggleBaseMap, setToggleBaseMap] = useState<BasemapToggle[]>(
        DEFAULT_BASEMAP_TOGGLE,
    );
    const currentBaseMapUrl = basemapUrl(toggleBaseMap);
    const layers = getLayers(toggleLayers);

    useEffect(() => {
        if (
            gotoLocation &&
            isValidCoordinate(gotoLocation.latitude, gotoLocation.longitude)
        ) {
            let newMapView = {
                ...initialView,
                longitude: gotoLocation.longitude,
                latitude: gotoLocation.latitude,
            };
            setInitialView(newMapView);
        }
    }, [gotoLocation]);

    return (
        <>
            <div className={styles.searchBox}>
                <SearchWidget updateGoToCoords={setGotoLocation} />
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
                initialViewState={initialView}
                controller={{ scrollZoom: true }}
                layers={layers}
            >
                <Map
                    initialViewState={initialView}
                    mapStyle={currentBaseMapUrl}
                    mapboxAccessToken={MAPBOX_PUBLIC_TOKEN}
                    style={{ width: '500px', height: '500px' }}
                    attributionControl={false}
                />
            </DeckGL>
        </>
    );
}
