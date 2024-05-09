// this is our common search input that will be used in a lot of other components
import React, { useState } from 'react';
import { TextInput, CloseButton } from '@mantine/core';
import styles from './SearchWidget.module.css';
import { IconSearch } from '@tabler/icons-react';

export default function SearchWidget() {
    const [value, setValue] = useState(""); 

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setValue(event.target.value); 
    }

    const clearInput = () => {
        setValue('');
    }
    const icon = <IconSearch className={styles.icon} />;
    return (
        <>
            <div className={styles.container}>
                <TextInput
                    leftSection={icon}
                    placeholder="Search Location Here"
                    onChange={(event) => handleInputChange(event)}
                    value={value}
                    rightSection={
                        <CloseButton 
                            aria-label='Clear Input'
                            onClick={() => clearInput()}
                            style={{ display: value ? undefined : 'none' }}
                        />
                    }
                />
            </div>
        </>
    );
}
