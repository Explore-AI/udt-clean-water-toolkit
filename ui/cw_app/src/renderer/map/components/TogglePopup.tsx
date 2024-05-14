import * as styles from '../css/TogglePopup.module.css';
import { Stack, Checkbox } from '@mantine/core';
import { useListState } from '@mantine/hooks';
import { UseListStateHandlers } from '@mantine/hooks';
import {
    LayerToggleObject,
    LayerToggle,
    BasemapToggleObject,
} from '../types/types';
interface ToggleProps {
    toggleList: LayerToggle[];
}

// create a function that creates a list of Checkbox items in array
const generateCheckbox = (
    toggleObject: LayerToggle[],
    handlers: UseListStateHandlers<LayerToggle>,
) => {
    return toggleObject.map((toggle: LayerToggle, index: number) => {
        return (
            <Checkbox
                key={toggle.key}
                label={toggle.label}
                checked={toggle.visible}
                onChange={(event) => {
                    handlers.setItemProp(
                        index,
                        'visible',
                        event.currentTarget.checked,
                    );
                }}
            />
        );
    });
};

export default function ToggleViewPopup({ toggleList }: ToggleProps) {
    /*
        This component accepts the following: 
            - an object of type string:bool
            - A function that will change the value of that string:bool
    */
    const [values, handlers] = useListState(toggleList);

    const checkBoxList = generateCheckbox(values, handlers);

    return (
        <>
            <div className={styles.container}>
                {/* <p> Here is a toggle popup window </p> */}
                {checkBoxList}
            </div>
        </>
    );
}
