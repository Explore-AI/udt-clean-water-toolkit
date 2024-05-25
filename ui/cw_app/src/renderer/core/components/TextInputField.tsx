// this is our common search input that will be used in a lot of other components
import { useState } from 'react';
import { TextInput, CloseButton } from '@mantine/core';

function TextInputField(props) {

    const { defaultValue, onChange, onClose, onEnter, classNames, showCloseButton } = props

    const [ value, setValue ] = useState(defaultValue || '')

    const handleChange = (e) => {
        const newValue = e.target.value
        setValue(newValue)
        onChange && onChange(newValue)
    }

    const handleKeyDown = (e) => {
        if(e.key === 'Enter') {
            onEnter && onEnter(e.target.value);
        }
    }

    const handleClose = () => {
        setValue('')
        onClose && onClose()
    }

    return (
        <TextInput
            placeholder="Search coordinates, address, or assets...."
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            classNames={classNames}
            value={value}
            rightSection={
            value &&
            showCloseButton &&
            <CloseButton
                aria-label="Clear Input"
                onClick={handleClose}
            />
            }
        />
    );
}

export default TextInputField
