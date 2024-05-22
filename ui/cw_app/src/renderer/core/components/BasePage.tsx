import { MantineProvider } from '@mantine/core';
import BaseRouter from './BaseRouter'
import {
    QueryClient,
    QueryClientProvider,
} from '@tanstack/react-query'
import '@mantine/core/styles.css';

const queryClient = new QueryClient()

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
