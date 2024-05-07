import { MemoryRouter as Router, Routes, Route } from 'react-router-dom';
import { Outlet } from 'react-router-dom';
import icon from '../../assets/icon.svg';
import './App.css';
import Header from './features/common/Header';
import MapPage from './features/map/MapPage';



export default function App() {
  return (
    <>
        <Header />
        <MapPage />
    </>
  );
}
