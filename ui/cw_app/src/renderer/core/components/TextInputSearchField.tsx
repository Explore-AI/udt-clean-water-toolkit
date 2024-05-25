import styles from '../css/TextInputSearchField.module.css'
import { useState } from 'react';
import { TextInput, CloseButton } from '@mantine/core';
import { IconSearch } from '@tabler/icons-react';

function TextInputSearchField(props) {

    const {
        defaultValue,
        onChange,
        onClose,
        onEnter,
        placeholder,
        classNames,
        showClearButton,
    } = props;

    const [value, setValue] = useState(defaultValue || '');

    const handleChange = (e) => {
        const newValue = e.target.value;
        setValue(newValue);
        onChange && onChange(newValue);
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            onEnter && onEnter(e.target.value);
        }
    };

    const handleClose = () => {
        setValue('');
        onClose && onClose();
    };

    return (
        <TextInput
            placeholder={placeholder}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            classNames={classNames}
            value={value}
            rightSection={
            value &&
            showClearButton && (
                <>
                    <CloseButton
                        aria-label="Clear Input"
                        onClick={handleClose}
                    />
                    <IconSearch className={styles.icon} />
                </>
            )}
        />
    );
}

export default TextInputSearchField;
