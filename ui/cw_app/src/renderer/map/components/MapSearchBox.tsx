// this is our common search input that will be used in a lot of other components
import styles from '../css/MapSearchBox.module.css';
import axios from 'axios';
import { TextInput, CloseButton } from '@mantine/core';
import { IconSearch, IconAlertTriangle } from '@tabler/icons-react';
import { validateInput, getNominatimData } from '../../core/utils/utils';



export default function MapSearchBox() {


    const icon = <IconSearch className={styles.icon} />;
    const errorIcon = (
        <IconAlertTriangle
            stroke={1.5}
            className={`${styles.icon} ${styles.errorIcon}`}
        />
    );

    const getLocation = async ({ payload, type }: GoToProps) => {
        const addressProps = {
            urlExtension: 'search',
            params: {
                q: payload as string,
                format: 'jsonv2',
                limit: 1,
                addressdetails: 1,
            },
        };
        const addressData = await getNominatimData(addressProps);
        return addressData;
    };

    const onSearch = async (e) => {
        const validInput = validateInput(e.target.value);
        if (!validInput?.validated) {
            //setHasError(true);
            return;
        } else {
            //setHasError(false);
            // set the go to location
            if (validInput.type == 'gps') {
                updateGoToCoords({
                    latitude: validInput.payload[0] as number,
                    longitude: validInput.payload[1] as number,
                });
            } else {
                const goToLocation = await getLocation(validInput);
                updateGoToCoords({
                    latitude: goToLocation.lat,
                    longitude: goToLocation.lon,
                });
            }
        }
    }

    return (
        <div className={styles.box}>
            <TextInput
                placeholder="Search coordinates, address, or assets...."
                onChange={onSearch}
                classNames={{ input: styles.input }}
                rightSection={
                    <CloseButton
                        aria-label="Clear Input"
                        onClick={() => {}}
                    />
                }
            />
            <button type="submit" className={styles.submitButton}>
                {icon}
            </button>
        </div>
    );
}
