// create a widget that will be used to provide GeoSpatial Control
import styles from '../css/MapLayerControl.module.css';
import useMapLayers from '../hooks/useMapLayers';
import useMapUi from '../hooks/useMapUi';
import { map as _map } from 'lodash';
import { Checkbox, Tooltip, ActionIcon, rem } from '@mantine/core';
import { IconMap } from '@tabler/icons-react';

export default function MapBaseLayerControl() {
    const { uiParams, setMapUiParams } = useMapUi();

    const { mapLayerProps, setMapLayerProps } = useMapLayers();

    const onIconClick = () => {
        setMapUiParams({
            showBaseLayerControls: !uiParams.showBaseLayerControls,
        })
    }

    return (
        <>
            <Tooltip label="Toggle Base Map">
                <ActionIcon
                    className={styles.button}
                    onClick={onIconClick}
                    size={42}>
                    <IconMap
                        style={{ width: rem(42), height: rem(42) }}
                        stroke={1.5}
                    />
                </ActionIcon>
            </Tooltip>

            {uiParams.showBaseLayerControls && (
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

/* {showBaseMapToggle && (
 *     <div className={styles.basemapTogglePopup}>
 *         <BasePopup>
 *             <RadioButtonList
 *                 toggleList={toggleBaseMap}
 *                 setToggleList={setToggleBaseMap}
 *             />
 *         </BasePopup>
 *     </div>
 * )} */

/* <Tooltip label="Toggle Base Map">
 *     <ActionIcon
 *         className={styles.button}
 *         onClick={handleBasemapToggleClick}
 *         size={42}
 *     >
 *         <IconMap
 *             style={{ width: rem(42), height: rem(42) }}
 *             stroke={1.5}
   />
   </ActionIcon>
   </Tooltip> */
