import '@mantine/core/styles.css';
import { MantineProvider } from '@mantine/core';
import BaseRouter from './BaseRouter'
import { QueryClientProvider } from '@tanstack/react-query'
import { queryClient } from '../'

function BasePage() {

    return (
        <MantineProvider>
            <QueryClientProvider client={queryClient}>
                <BaseRouter/>
            </QueryClientProvider>
        </MantineProvider>
    );
}

export default BasePage;
