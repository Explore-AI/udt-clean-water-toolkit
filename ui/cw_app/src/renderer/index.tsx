// our main app file
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { createTheme, MantineProvider } from '@mantine/core';
import App from './App';
import NotFoundErrorPage from './features/common/NotFoundErrorPage';
import MapPage from './features/map/MapPage';
import '@mantine/core/styles.css';

const theme = createTheme({
  fontFamily: 'Open Sans, sans-serif',
  primaryColor: 'cyan',
});

// router navigation to be expanded upon
const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    errorElement: <NotFoundErrorPage />,
  },
]);


const container = document.getElementById('root') as HTMLElement;
const root = createRoot(container);
root.render(
  <MantineProvider> 
    <App />
  </MantineProvider>
  
);

// calling IPC exposed from preload script
window.electron.ipcRenderer.once('ipc-example', (arg) => {
  // eslint-disable-next-line no-console
  console.log(arg);
});
window.electron.ipcRenderer.sendMessage('ipc-example', ['ping']);
