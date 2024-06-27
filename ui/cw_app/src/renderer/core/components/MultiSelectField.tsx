import { useState } from 'react';
import { MultiSelect } from '@mantine/core';

const MultiSelectField = (props) => {
    const {
        label,
        placeholder,
        data,
        labelName,
        searchable,
        clearable,
        onSearchChange,
        onEnter,
        maxValues 
    } = props;

    const [options, setOptions] = useState([]);
    const [ dropdownOpened, setDropdownOpened ] = useState(false); 

    const handleChange = (values) => {
        setOptions(values);
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            onEnter && onEnter(options);
            setDropdownOpened(false);
        }
    };

    return (
        <MultiSelect
            label={label}
            clearable={clearable}
            placeholder={placeholder}
            onSearchChange={onSearchChange}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            searchable={searchable}
            renderOption={(item) =>
                item.option[labelName] || item.option['value']
            }
            data={data}
            hidePickedOptions
            maxValues={maxValues}
            onDropdownOpen={() => setDropdownOpened(true)}
            dropdownOpened={dropdownOpened}
        />
    );
};

export default MultiSelectField;
