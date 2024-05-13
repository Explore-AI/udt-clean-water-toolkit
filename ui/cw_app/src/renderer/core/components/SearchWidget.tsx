// this is our common search input that will be used in a lot of other components
import React, { useState } from 'react';
import { TextInput, CloseButton } from '@mantine/core';
import styles from '../css/SearchWidget.module.css';
//import { IconSearch } from '@tabler/icons-react';

export default function SearchWidget() {
  const [value, setValue] = useState();

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setValue(e.target.value);
  }

  const onClear = () => {
    setValue();
  }
  //    const icon = <IconSearch className={styles.icon} />;
  return (
    <TextInput
      placeholder="Search"
      onChange={(e) => onChange(e)}
      value={value}
      classNames={{ input: styles.input}}
      rightSection={
        <CloseButton
          aria-label='Clear Input'
          onClick={() => onClear()}
          style={{ display: value ? undefined : 'none' }}
        />
      }
    />
  );
}
