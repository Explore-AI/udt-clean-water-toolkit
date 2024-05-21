// create a widget that will be used to provide GeoSpatial Control
import styles from '../css/MapLayerControl.module.css';
import { useContext } from 'react';
import useMapLayers from '../hooks/useMapLayers';
import useMapUi from '../hooks/useMapUi';
import { map as _map } from 'lodash';
import { Checkbox, Tooltip, ActionIcon, rem } from '@mantine/core';
import { IconMap } from '@tabler/icons-react';
import { DEFAULT_BASEMAP_PROPS } from '../../core'
import { MapUiContext } from '../hooks/useMapUi';

export default function MapBaseLayerControl() {

    const { uiParams, setMapUiParams } = useContext(MapUiContext);

    const { mapLayerProps, setMapLayerProps, setBaseMapUrl } = useMapLayers();

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
                    {_map(DEFAULT_BASEMAP_PROPS, (layerProps) => {
                        return (
                            <Checkbox
                                key={layerProps.key}
                                label={layerProps.label}
                                defaultChecked={layerProps.visible}
                                onChange={() => setBaseMapUrl(layerProps.map_url)}
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
