// our main app file
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, RouterProvider, createHashRouter } from 'react-router-dom';
import { createTheme, MantineProvider } from '@mantine/core';
import App from './App';
import NotFoundErrorPage from './features/common/NotFoundErrorPage';
import MapPage from './features/map/MapPage';
import GraphViewPage from './features/graph/GraphPage';
import SchematicViewPage from './features/schematic/SchematicPage';
import AnalysisViewPage from './features/analysis/AnalysisPage';
import '@mantine/core/styles.css';

const theme = createTheme({
    fontFamily: 'Open Sans, sans-serif',
    primaryColor: 'cyan',
});

// use HashRouter as it is meant for file based environments
const router = createHashRouter([
    {
        path: '/',
        element: <App />,
        errorElement: <NotFoundErrorPage />,
        children: [
            {
                element: <MapPage />,
                index: true, 
            },
            {
                element: <GraphViewPage />,
                path: '/graph',
            }, 
            {
                element: <GraphViewPage />,
                path: '/geo-graph',
            }, 
            {
                element: <SchematicViewPage />,
                path: '/schematic',
            }, 
            {
                element: <AnalysisViewPage />,
                path: '/analysis',
            }
        ],
    },
]);

const container = document.getElementById('root') as HTMLElement;
const root = createRoot(container);
root.render(
    <MantineProvider>
        <RouterProvider router={router} />
    </MantineProvider>,
);

// calling IPC exposed from preload script
window.electron.ipcRenderer.once('ipc-example', (arg) => {
    // eslint-disable-next-line no-console
    console.log(arg);
});
window.electron.ipcRenderer.sendMessage('ipc-example', ['ping']);
