import { Route, Routes, Navigate } from 'react-router-dom';
import MapPage from '../../map/components/MapPage';
import Graph from '../../graph/components/GraphPage';
import AnalysisPage from '../../analysis/components/AnalysisPage';

function BaseRouter() {
    console.log('aaaa');
    return (
        <Routes>
            <Route path="/" element={<Navigate to="/map" replace={true} />} />
            <Route path="/map/:latlong?" element={<MapPage />} />
            <Route path="/graph" element={<Graph />} />
            <Route path="/analysis" element={<AnalysisPage />} />
        </Routes>
    );
}

export default BaseRouter;

/* <Route path="map">
 * <Route path=":latlong" element={<MapPage />} />
 * </Route> */
