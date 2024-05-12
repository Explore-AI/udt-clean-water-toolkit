import { Route, Routes } from 'react-router-dom';
import Map from '../../map/components/MapPage'

function BaseRouter() {
  return (
    <Routes>
      <Route path="/" exact={true} element={<Map/>} />
      <Route path="/graph" exact={true} element={<Map/>} />
    </Routes>
  );
}

export default BaseRouter;
