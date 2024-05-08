import App from './App';
import NotFoundErrorPage from './features/common/NotFoundErrorPage';
import MapPage from './features/map/MapPage';
import GraphViewPage from './features/graph/GraphPage';
import SchematicViewPage from './features/schematic/SchematicPage';
import AnalysisViewPage from './features/analysis/AnalysisPage';
import {
    createHashRouter,
} from 'react-router-dom';
// use HashRouter as it is meant for file based environments
const router = createHashRouter([
    {
        path: '/',
        element: <App />,
        errorElement: <NotFoundErrorPage />,
        children: [
            {
                element: <MapPage />,
                index: true,
            },
            {
                element: <GraphViewPage />,
                path: '/graph',
            },
            {
                element: <GraphViewPage/>,
                path: '/geo-graph',
            },
            {
                element: <SchematicViewPage />,
                path: '/schematic',
            },
            {
                element: <AnalysisViewPage />,
                path: '/analysis',
            },
        ],
    },
]);

export { router }; 