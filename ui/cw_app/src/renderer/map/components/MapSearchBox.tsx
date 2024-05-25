// this is our common search input that will be used in a lot of other components
import styles from '../css/MapSearchBox.module.css';
//import { useState, useEffect } from 'react';
import TextInputField from '../../core/components/TextInputField'
import { useNavigate } from "react-router-dom";
/* import { IconSearch, IconAlertTriangle } from '@tabler/icons-react';
 * import { validateInput, getNominatimData } from '../../core/utils/utils';
 * import {
 *     useInitialView,
 *     useLayerToggle,
 *     useBasemapToggle,
 *     useGoToLocation,
 * } from '../hooks/useMapContext';
 * import { isValidCoordinate } from '../../core/utils/utils'; */

export default function MapSearchBox() {

    const navigate = useNavigate();

    const onSearch = async (value) => {
        if (value) {
            navigate(`/map/${value}`)
        } else {
            navigate(`/map`)
        }
    }

    return (
        <div className={styles.box}>
            <TextInputField
                onEnter={onSearch}
                classNames={{ input: styles.input }}
                showCloseButton={true}
            />
        </div>
    );
}
