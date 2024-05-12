import { Route, Routes } from 'react-router-dom';
import Map from '../../map/components/MapPage'
import Graph from '../../graph/components/GraphPage'

function BaseRouter() {
  return (
    <Routes>
      <Route path="/" exact={true} element={<Map/>} />
      <Route path="/graph" exact={true} element={<Graph/>} />
    </Routes>
  );
}

export default BaseRouter;
