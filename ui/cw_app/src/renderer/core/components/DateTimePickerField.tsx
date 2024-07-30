import { DateTimePicker, DatesProvider } from '@mantine/dates';

const DateTimePickerField = () => {

    return (
        <>
            <DatesProvider settings={{ consistentWeeks: true }}>
                <DateTimePicker
                    valueFormat="DD MMM YYYY HH:mm"
                    placeholder="Pick a Date & Time"
                    clearable={true}
                    defaultValue={new Date()}
                />
            </DatesProvider>
        </>
    );
};

export default DateTimePickerField
