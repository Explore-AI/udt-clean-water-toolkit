// this is our common search input that will be used in a lot of other components
import { useState } from 'react';
import { TextInput, CloseButton } from '@mantine/core';

function TextInputField(props) {

    const { defaultValue, onChange, onEnter, classNames, showCloseButton } = props

    const [ value, setValue ] = useState(defaultValue)

    const handleChange = (e) => {
        console.log(e)
        const newValue = e.target.value
        setValue(newValue)
        onChange && onChange(newValue)
    }

    const handleKeyDown = (e) => {
        if(e.key === 'Enter') {
            onEnter && onEnter(e.target.value);
        }
    }

    return (
        <TextInput
            placeholder="Search coordinates, address, or assets...."
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            classNames={classNames}
            rightSection={
            showCloseButton &&
            <CloseButton
                aria-label="Clear Input"
                onClick={() => {}}
            />
            }
        />
    );
}

export default TextInputField
