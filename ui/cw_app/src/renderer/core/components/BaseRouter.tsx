import { Route, Routes, Navigate } from 'react-router-dom';
import BaseLayout from '../../core/components/BaseLayout';
import BaseSinglePage from './BaseSinglePage'

const BaseRouter = () => {

    return (
        <BaseLayout>
            <Routes>
                <Route path="/" element={<Navigate to="/map" replace={true} />} />
                <Route path="/map/:latlong?" element={<BaseSinglePage />} />
                <Route path="/graph" element={<BaseSinglePage/>} />
                <Route path="/schematic" element={<BaseSinglePage/>} />
                <Route path="/analysis" element={<BaseSinglePage/>} />
                <Route path="/geo-graph" element={<BaseSinglePage/>} />
            </Routes>
        </BaseLayout>
    );
}

export default BaseRouter;
