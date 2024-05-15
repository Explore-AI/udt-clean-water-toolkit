// create a widget that will be used to provide GeoSpatial Controls
import { Button, Tooltip } from '@mantine/core';
import * as styles from '../css/MapControl.module.css';
import { useContext } from 'react';
import { MapContext } from '../context/MapContext';

export default function GeoSpatialControls({}) {
    const {
        showLayerToggle,
        setShowLayerToggle,
        showBaseMapToggle,
        setShowBaseMapToggle,
    } = useContext(MapContext);
    const handleLayerToggleClick = () => {
        setShowLayerToggle(!showLayerToggle);
        setShowBaseMapToggle(false);
    };

    const handleBasemapToggleClick = () => {
        setShowBaseMapToggle(!showBaseMapToggle);
        setShowLayerToggle(false);
    };
    
    return (
        <>
            <Tooltip label="Toggle Layers">
                <Button
                    onClick={handleLayerToggleClick}
                    className={styles.button}
                >
                    Layer Popup
                </Button>
            </Tooltip>

            <Tooltip label='Toggle Base Map'>
                <Button
                    onClick={handleBasemapToggleClick}
                    className={styles.button}
                >
                    BaseMap Popup
                </Button>
            </Tooltip>
        </>
    );
}
