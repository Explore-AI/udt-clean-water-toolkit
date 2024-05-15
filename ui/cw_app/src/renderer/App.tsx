import { createRoot } from 'react-dom/client';
import { router as AppRouter } from './routes';
import { HashRouter as Router } from 'react-router-dom';
import {  RouterProvider } from 'react-router-dom';
import { MantineProvider } from '@mantine/core';
import '@mantine/core/styles.css';
import BasePage from './core/components/BasePage';

export default function App() {
  return (
    <Router>
      <BasePage />
    </Router>
  );
}
