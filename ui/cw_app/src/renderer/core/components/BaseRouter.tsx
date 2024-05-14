import { Route, Routes } from 'react-router-dom';
import Map from '../../map/components/MapPage'
import Graph from '../../graph/components/GraphPage'
import AnalysisPage from '../../analysis/components/AnalysisPage'

function BaseRouter() {
  return (
    <Routes>
      <Route path="/" element={<Map/>} />
      <Route path="/graph" element={<Graph/>} />
      <Route path="/analysis" element={<AnalysisPage/>} />
    </Routes>
  );
}

export default BaseRouter;
