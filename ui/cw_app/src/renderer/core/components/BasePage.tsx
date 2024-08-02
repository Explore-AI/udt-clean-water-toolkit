import '@mantine/core/styles.css';
import 'mantine-react-table/styles.css'; //import MRT styles
import '@mantine/dates/styles.css';
import { MantineProvider } from '@mantine/core';
import BaseRouter from './BaseRouter'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

export const queryClient = new QueryClient()

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
