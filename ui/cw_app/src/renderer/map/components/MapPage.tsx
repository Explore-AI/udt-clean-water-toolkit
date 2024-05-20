// Our Map Page details exists here
import React, { useState } from 'react';
import styles from '../css/MapPage.module.css';
import MapView from './MapView';
import BaseLayout from '../../core/components/BaseLayout';
import useMapUi, { MapUiContext } from '../hooks/useMapUi';

function MapPage() {
    const { showLayerToggle, showBaseMapToggle } = useMapUi();

    return (
        <BaseLayout>
            <MapUiContext.Provider value={(showLayerToggle, showBaseMapToggle)}>
                <div className={styles.pageContainer}>
                    <MapView />
                </div>
            </MapUiContext.Provider>
        </BaseLayout>
    );
}

export default MapPage;
