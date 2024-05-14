// create a widget that will be used to provide GeoSpatial Controls
import { Button } from '@mantine/core';
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
        console.log('Toggle Layer clicked');
        setShowLayerToggle(!showLayerToggle);
        setShowBaseMapToggle(false);
    };

    const handleBasemapToggleClick = () => {
        console.log('Toggle Basemap clicked');
        setShowBaseMapToggle(!showBaseMapToggle);
        setShowLayerToggle(false); 
    };
    // console.log('Show the Layer Toggle: ', showLayerToggle)
    // console.log('Show the Base Map Toggle: ', showBaseMapToggle)
    return (
        <>
            <Button
                variant="primary"
                onClick={handleLayerToggleClick}
                className={styles.button}
            >
                Layer Popup
            </Button>

            <Button
                onClick={handleBasemapToggleClick}
                className={styles.button}
            >
                BaseMap Popup
            </Button>
        </>
    );
}
