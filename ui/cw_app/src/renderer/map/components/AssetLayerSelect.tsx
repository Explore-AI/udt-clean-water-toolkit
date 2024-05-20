// create a widget that will be used to provide GeoSpatial Controls
import { Tooltip, ActionIcon, rem } from '@mantine/core';
import styles from '../css/MapControl.module.css';
import { IconStack2 } from '@tabler/icons-react';

export default function AssetLayerSelect() {
    return (
        <>
            <Tooltip label="Toggle Layers">
                <ActionIcon className={styles.button} onClick={} size={42}>
                    <IconStack2
                        style={{ width: rem(42), height: rem(42) }}
                        stroke={1.5}
                    />
                </ActionIcon>
            </Tooltip>
            <div className={styles.layerTogglePopup}>
                <BasePopup>
                    <CheckboxList
                        toggleList={toggleLayers}
                        setToggleList={setToggleLayers}
                    />
                </BasePopup>
            </div>
            )
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
