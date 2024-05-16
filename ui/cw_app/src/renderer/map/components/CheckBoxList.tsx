import React from 'react';
import { Checkbox } from '@mantine/core';
import styles from '../css/CheckBoxList.module.css';
import { LayerToggle } from '../types/types';

interface CheckboxListProps {
    toggleList: LayerToggle[];
    setToggleList: React.Dispatch<React.SetStateAction<LayerToggle[]>>;
}

export default function CheckboxList({
    toggleList,
    setToggleList,
}: CheckboxListProps) {
    const content = toggleList.map((toggle: LayerToggle, index: number) => {
        return (
            <Checkbox
                key={toggle.key}
                label={toggle.label}
                checked={toggle.visible}
                classNames={{
                    root: styles.checkBoxItem,
                    input: styles.checkBoxInput,
                }}
                onChange={(event) => {
                    const newToggleObject = [...toggleList];
                    newToggleObject[index] = {
                        ...toggle,
                        visible: event.currentTarget.checked,
                    };
                    setToggleList(newToggleObject);
                }}
            />
        );
    });
    return <>{content}</>;
}
