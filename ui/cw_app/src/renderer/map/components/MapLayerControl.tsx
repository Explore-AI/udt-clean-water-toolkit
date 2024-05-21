// create a widget that will be used to provide GeoSpatial Control
import styles from '../css/MapLayerControl.module.css';
import { useContext } from 'react';
import { map as _map } from 'lodash';
import { Checkbox, Tooltip, ActionIcon, rem } from '@mantine/core';
import { IconStack2 } from '@tabler/icons-react';
import { MapLayerContext } from '../hooks/useMapLayers';
import { MapUiContext } from '../hooks/useMapUi';

export default function MapLayerControl() {

    const { uiParams, setMapUiParams } = useContext(MapUiContext);
    const { mapLayerProps, setMapLayerProps } = useContext(MapLayerContext);

    const onIconClick = () => {
        setMapUiParams({
            showLayerControls: !uiParams.showLayerControls,
        });
    };

    return (
        <>
            <Tooltip label="Toggle Layers">
                <ActionIcon
                    className={styles.button}
                    onClick={onIconClick}
                    size={42}
                >
                    <IconStack2
                        style={{ width: rem(42), height: rem(42) }}
                        stroke={1.5}
                    />
                </ActionIcon>
            </Tooltip>

            {uiParams.showLayerControls && (
                <div className={styles.control_box}>
                    {_map(mapLayerProps, (layerProps) => {
                        return (
                            <Checkbox
                                key={layerProps.key}
                                label={layerProps.label}
                                defaultChecked={layerProps.visible}
                                onChange={(e) => {
                                    setMapLayerProps({
                                        ...layerProps,
                                        visible: e.currentTarget.checked,
                                    });
                                }}
                            />
                        );
                    })}
                </div>
            )}
        </>
    );
}
