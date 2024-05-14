import { HashRouter as Router } from 'react-router-dom';
import '@mantine/core/styles.css';
import BasePage from './core/components/BasePage';

export default function App() {
  return (
    <Router>
      <BasePage />
    </Router>
  );
}
