// create a widget that will be used to provide GeoSpatial Controls
import { Button, Tooltip, ActionIcon, rem } from '@mantine/core';
import * as styles from '../css/MapControl.module.css';
import { useContext } from 'react';
import { MapContext } from '../context/MapContext';
import { IconMap, IconStack2 } from '@tabler/icons-react';

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
                <ActionIcon
                    className={styles.button}
                    onClick={handleLayerToggleClick}
                    size={42}
                >
                    <IconStack2
                        style={{ width: rem(42), height: rem(42) }}
                        stroke={1.5}
                    />
                </ActionIcon>
            </Tooltip>

            <Tooltip label="Toggle Base Map">
                <ActionIcon
                    className={styles.button}
                    onClick={handleBasemapToggleClick}
                    size={42}
                >
                    <IconMap
                        style={{ width: rem(42), height: rem(42) }}
                        stroke={1.5}
                    />
                </ActionIcon>
            </Tooltip>
        </>
    );
}
