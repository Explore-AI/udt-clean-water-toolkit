// this is our common search input that will be used in a lot of other components
import React, { useState } from 'react';
import { TextInput, CloseButton } from '@mantine/core';
import styles from '../css/SearchWidget.module.css';
import { IconSearch } from '@tabler/icons-react';

export default function SearchWidget() {
    const [value, setValue] = useState<string>('');

    const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setValue(e.target.value);
    };

    const onClear = () => {
        setValue('');
    };

    const handleSubmission = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (value == '')
            console.log('please enter a value');
        console.log(value);
    }

    const icon = <IconSearch className={styles.icon} />;
    return (
        <>
            <form>
                <TextInput
                    placeholder="Search coordinates, address, or assets...."
                    leftSection={icon}
                    onChange={(e) => onChange(e)}
                    value={value}
                    classNames={{ input: styles.input }}
                    rightSection={
                        <CloseButton
                            aria-label="Clear Input"
                            onClick={() => onClear()}
                            style={{ display: value ? undefined : 'none' }}
                        />
                    }
                />
            </form>
        </>
    );
}
