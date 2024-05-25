// this is our common search input that will be used in a lot of other components
import styles from '../css/MapSearchBox.module.css';
import TextInputField from '../../core/components/TextInputField'
import { IconSearch } from '@tabler/icons-react';
import { useNavigate } from "react-router-dom";
import { validateInput, getNominatimData } from '../../core/utils/utils';
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
            const validatedInput = validateInput(value);
            if (validatedInput.type == 'gps') {
                navigate(`/map/${validatedInput.payload[0]},${validatedInput.payload[1]}`)
            } else {
                const addressProps = {
                    urlExtension: 'search',
                    params: {
                        q: validatedInput.payload as string,
                        format: 'jsonv2',
                        limit: 1,
                        addressdetails: 1,
                    },
                };
                const addressData = await getNominatimData(addressProps)
                navigate(`/map/${addressData.lat},${addressData.lon}`)
            }
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
                onClose={() => navigate(`/map`)}
            />
        </div>
    );
}


{/* <IconSearch className={styles.icon} />; */}
