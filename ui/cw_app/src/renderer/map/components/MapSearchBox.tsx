// this is our common search input that will be used in a lot of other components
import React, { useState, SetStateAction } from 'react';
import { TextInput, CloseButton } from '@mantine/core';
import styles from '../css/MapSearchBox.module.css';
import { IconSearch, IconAlertTriangle } from '@tabler/icons-react';
import { validateInput, getNominatimData } from '../utils/utils';



export default function MapSearchBox() {


    const icon = <IconSearch className={styles.icon} />;
    const errorIcon = (
        <IconAlertTriangle
            stroke={1.5}
            className={`${styles.icon} ${styles.errorIcon}`}
        />
    );

    const onSearch = (e) => {
        console.log(e.target.value)
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
