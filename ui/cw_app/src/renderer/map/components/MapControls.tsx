// create a widget that will be used to provide GeoSpatial Controls
import { Tooltip, ActionIcon, rem } from '@mantine/core';
import styles from '../css/MapControl.module.css';
import { useLayerToggle, useBasemapToggle } from '../hooks/useMapContext';
import { IconMap, IconStack2 } from '@tabler/icons-react';
import AssetLayerSelect from './AssetLayerSelect';

export default function MapControls({}) {
    return <AssetLayerSelect />;
}
