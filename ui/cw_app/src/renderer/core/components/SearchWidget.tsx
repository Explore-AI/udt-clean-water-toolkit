// this is our common search input that will be used in a lot of other components
import React, { useState, SetStateAction } from 'react';
import { TextInput, CloseButton, Tooltip, ActionIcon } from '@mantine/core';
import styles from '../css/SearchWidget.module.css';
import { IconSearch, IconAlertTriangle } from '@tabler/icons-react';
import { validateInput, getNominatimData } from '../utils/utils';

type GoToProps = {
    payload: Number[] | string;
    type: string;
    validated: boolean;
};

type SearchProps = {
    updateGoToCoords: React.Dispatch<
        SetStateAction<{ latitude: number; longitude: number }>
    >;
};

export default function SearchWidget({ updateGoToCoords }: SearchProps) {
    const [value, setValue] = useState<string>('');
    const [hasError, setHasError] = useState<boolean>(false);

    const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setValue(e.target.value);
        setHasError(false);
    };

    const onClear = () => {
        setValue('');
        setHasError(false); 
    };

    const handleSubmission = async (
        event: React.FormEvent<HTMLFormElement>,
    ) => {
        event.preventDefault();
        const validInput = validateInput(value);
        if (!validInput?.validated) {
            setHasError(true);
            return;
        } else {
            setHasError(false);
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
    };

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

    const icon = <IconSearch className={styles.icon} />;
    const errorIcon = (
            <IconAlertTriangle
                stroke={1.5}
                className={`${styles.icon} ${styles.errorIcon}`}
            />
    );

    return (
        <>
            <form
                onSubmit={handleSubmission}
                className={`${styles.formContainer} ${hasError ? styles.errorInput : ''}`}
            >
                <TextInput
                    placeholder="Search coordinates, address, or assets...."
                    onChange={(e) => onChange(e)}
                    value={value}
                    classNames={{ input: styles.input }}
                    rightSection={
                        hasError ? (
                            errorIcon
                        ) : (
                            <CloseButton
                                aria-label="Clear Input"
                                onClick={() => onClear()}
                                style={{ display: value ? undefined : 'none' }}
                            />
                        )
                    }
                />
                <button type="submit" className={styles.submitButton}>
                    {icon}
                </button>
            </form>
        </>
    );
}
