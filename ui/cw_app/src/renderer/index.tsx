// our main app file
import { createRoot } from 'react-dom/client';
import {
    RouterProvider,
} from 'react-router-dom';
import { createTheme, MantineProvider } from '@mantine/core';
import '@mantine/core/styles.css';


import { router as AppRouter } from './routes';

const theme = createTheme({
    fontFamily: 'Inter, sans-serif',
});



const container = document.getElementById('root') as HTMLElement;
const root = createRoot(container);
root.render(
    <MantineProvider>
        <RouterProvider router={AppRouter} />
    </MantineProvider>,
);

// calling IPC exposed from preload script
window.electron.ipcRenderer.once('ipc-example', (arg) => {
    // eslint-disable-next-line no-console
    console.log(arg);
});
window.electron.ipcRenderer.sendMessage('ipc-example', ['ping']);
