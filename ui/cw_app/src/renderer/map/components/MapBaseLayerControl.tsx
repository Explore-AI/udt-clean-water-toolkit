// create a widget that will be used to provide GeoSpatial Control
import styles from '../css/MapBaseLayerControl.module.css';
import { useContext } from 'react';
import { map as _map } from 'lodash';
import { Radio, Tooltip, ActionIcon, rem } from '@mantine/core';
import { IconMap } from '@tabler/icons-react';
import { DEFAULT_BASEMAP_PROPS } from '../utils/mapUtils';
import { MapLayerContext } from '../hooks/useMapLayers';
import { MapUiContext } from '../hooks/useMapUi';

export default function MapBaseLayerControl() {
    const { uiParams, setMapUiParams } = useContext(MapUiContext);
    const { baseMap, setBaseMap } = useContext(MapLayerContext);

    const onIconClick = () => {
        setMapUiParams({
            showBaseLayerControls: !uiParams.showBaseLayerControls,
        });
    };

    return (
        <>
            <Tooltip label="Toggle Base Map">
                <ActionIcon
                    className={styles.button}
                    onClick={onIconClick}
                    size={42}
                >
                    <IconMap
                        style={{ width: rem(42), height: rem(42) }}
                        stroke={1.5}
                    />
                </ActionIcon>
            </Tooltip>

            {uiParams.showBaseLayerControls && (
                <div className={styles.control_box}>
                    {_map(DEFAULT_BASEMAP_PROPS, (layer) => {
                        return (
                            <div className={styles.radio_box}>
                                <Radio
                                    key={layer.key}
                                    label={layer.label}
                                    checked={layer.mapUrl === baseMap.mapUrl}
                                    onChange={() => setBaseMap(layer)}
                                />
                            </div>
                        );
                    })}
                </div>
            )}
        </>
    );
}
