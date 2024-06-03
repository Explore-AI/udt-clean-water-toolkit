import { MultiSelect } from '@mantine/core';

const MultiSelectField = (props) => {

    const { label, placeholder, data, labelName } = props

    return (
        <MultiSelect
            label={label}
            placeholder={placeholder}
            renderOption={ (item) => item.option[labelName] || item.option['value'] }
            data={data}
        />
    );
}

export default MultiSelectField
