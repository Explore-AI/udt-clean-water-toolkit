import { DateTimePicker, DatesProvider } from '@mantine/dates';
import { ActionIcon } from '@mantine/core';
import { IconCalendarTime } from '@tabler/icons-react';
import { useState } from 'react';

export const DateTimeInput = () => {
    const [date, setDate] = useState<Date|null>(null);


    return (
        <>
            <DatesProvider settings={{ consistentWeeks: true }}>
                <DateTimePicker
                    valueFormat="DD MMM YYYY HH:mm"
                    placeholder="Pick a Date & Time"
                    clearable
                    defaultValue={new Date()}
                    value={date}
                    onChange={setDate}
                />
            </DatesProvider>
        </>
    );
};
