import * as styles from '../css/TogglePopup.module.css';
import { Stack, Checkbox, Radio, RadioGroup } from '@mantine/core';
import {
    LayerToggle,
    BasemapToggle,
} from '../types/types';
import React from 'react';

interface ToggleProps {
    toggleList: LayerToggle[] | BasemapToggle[];
    setToggleList: React.Dispatch<
        React.SetStateAction<LayerToggle[] | BasemapToggle[]>
    >;
    isLayerToggle: boolean;
}

// create a function that creates a list of Checkbox items in array
const generateCheckbox = (
    toggleList: LayerToggle[],
    setToggleList: React.Dispatch<React.SetStateAction<LayerToggle[]>>,
) => {
    return toggleList.map((toggle: LayerToggle, index: number) => {
        return (
            <Checkbox
                key={toggle.key}
                label={toggle.label}
                checked={toggle.visible}
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
};

const generateRadioButtons = (
    toggleList: BasemapToggle[],
    setToggleList: React.Dispatch<React.SetStateAction<BasemapToggle[]>>,
) => {
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
                />
            ))}
        </RadioGroup>
    );
};

export default function ToggleViewPopup({
    toggleList,
    setToggleList,
    isLayerToggle,
}: ToggleProps) {

    let toggleContents;
    if (isLayerToggle)
        toggleContents = generateCheckbox(
            toggleList as LayerToggle[],
            setToggleList as React.Dispatch<
                React.SetStateAction<LayerToggle[]>
            >,
        );
    else
        toggleContents = generateRadioButtons(
            toggleList as BasemapToggle[],
            setToggleList as React.Dispatch<
                React.SetStateAction<BasemapToggle[]>
            >,
        );

    return (
        <>
            <div className={styles.container}>{toggleContents}</div>
        </>
    );
}
