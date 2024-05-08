import { Outlet } from 'react-router-dom';
import './App.css';
import Header from './features/common/Header';



export default function App() {
  return (
    <>
        <Header />
        <div id="detail"> 
          <Outlet />
        </div>
    </>
  );
}
