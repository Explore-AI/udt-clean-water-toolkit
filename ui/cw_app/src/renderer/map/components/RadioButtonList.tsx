import React from 'react';
import { Radio, RadioGroup } from '@mantine/core';
import styles from '../css/RadioButtonList.module.css';
import { BasemapToggle } from '../types/types';

interface RadioButtonListProps {
    toggleList: BasemapToggle[];
    setToggleList: React.Dispatch<React.SetStateAction<BasemapToggle[]>>;
}

export default function RadioButtonList({toggleList, setToggleList}: RadioButtonListProps) {
    return (
        <RadioGroup
            value={toggleList.find((toggle) => toggle.visible)?.key}
            onChange={(value) => {
                setToggleList(
                    toggleList.map((toggle) => {
                        return {
                            ...toggle,
                            visible: toggle.key === value,
                        };
                    }),
                );
            }}
        >
            {toggleList.map((toggle: BasemapToggle) => (
                <Radio
                    key={toggle.key}
                    value={toggle.key}
                    label={toggle.label}
                    classNames={{
                        root: styles.radioGroupItem,
                        radio: styles.radioInput,
                    }}
                />
            ))}
        </RadioGroup>
    );
}