import styles from '../css/TextInputSearchField.module.css'
import { useState } from 'react';
import { TextInput, CloseButton } from '@mantine/core';
import { IconSearch, IconX } from '@tabler/icons-react';

function TextInputSearchField(props) {

    const {
        defaultValue,
        onChange,
        onClear,
        onSearch,
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

    const handleSearch = () => {
        onSearch && onSearch(value);

    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            handleSearch()
        }
    };

    const handleClear = () => {
        setValue('');
        onClear && onClear();
    };

    return (
        <TextInput
            placeholder={placeholder}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            classNames={classNames}
            value={value}
            rightSection={
                <>
            {value &&
             showClearButton &&
             <IconX
                 className={styles.clear}
                 onClick={handleClear}
             />
            }
                    <IconSearch
                        onClick={handleSearch}
                        className={styles.icon}
                    />
                </>
            }
        />
    );
}

export default TextInputSearchField;
