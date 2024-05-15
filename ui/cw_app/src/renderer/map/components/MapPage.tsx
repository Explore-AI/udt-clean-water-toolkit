// Our Map Page details exists here
import * as styles from '../css/MapPage.module.css';
import BaseLayout from '../../core/components/BaseLayout';
import MapView from './Map';
import { useState } from 'react';
import { MapContext } from '../context/MapContext';
import { INITIAL_VIEW_STATE } from '../../core';

export default function MapPage() {
    // set our state variables for our Map Page
    const [initialView, setInitialView] = useState(INITIAL_VIEW_STATE);
    const [showLayerToggle, setShowLayerToggle] = useState(false);
    const [showBaseMapToggle, setShowBaseMapToggle] = useState(false);

    const MapValues = {
        initialView,
        setInitialView,
        showLayerToggle,
        setShowLayerToggle,
        showBaseMapToggle,
        setShowBaseMapToggle,
    };

    return (
        <BaseLayout>
            <MapContext.Provider value={MapValues}>
                <div className={styles.pageContainer}>
                    <MapView />
                </div>
            </MapContext.Provider>
        </BaseLayout>
    );
}
