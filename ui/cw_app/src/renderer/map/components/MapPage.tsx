// Our Map Page details exists here
import React, { useState } from 'react';
import styles from '../css/MapPage.module.css';
import MapView from './MapView';
import MapLayout from '../../core/components/MapLayout';
import useMapUi, { MapUiContext } from '../hooks/useMapUi';

export default function MapPage() {
    const { showLayerToggle, showBaseMapToggle } = useMapUi();

    return (
        <MapLayout>
            <MapUiContext.Provider value={(showLayerToggle, showBaseMapToggle)}>
                <div className={styles.pageContainer}>
                    <MapView />
                </div>
            </MapUiContext.Provider>
        </MapLayout>
    );
}
