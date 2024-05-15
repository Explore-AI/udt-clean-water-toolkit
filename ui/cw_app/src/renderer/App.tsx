import { HashRouter as Router } from 'react-router-dom';
import BasePage from './core/components/BasePage';
import './core/css/index.css'; 

export default function App() {
  return (
    <Router>
      <BasePage />
    </Router>
  );
}
