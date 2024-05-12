import { createHashRouter } from 'react-router-dom';
import App from './App';
import NotFoundErrorPage from './core/components/NotFoundPage';
/* import MapPage from './map/components/MapPage';
 * import GraphViewPage from './graph/components/GraphPage';
 * import SchematicViewPage from './schematic/components/SchematicPage';
 * import AnalysisViewPage from './analysis/components/AnalysisPage'; */

// use HashRouter as it is meant for file based environments
const router = createHashRouter([
  {
        path: '/',
        element: <App />,
        errorElement: <NotFoundErrorPage />,
      /* children: [
       *     {
       *         element: <MapPage />,
       *         index: true,
       *     },
       *     {
       *         element: <GraphViewPage />,
       *         path: '/graph',
       *     },
       *     {
       *         element: <GraphViewPage/>,
       *         path: '/geo-graph',
       *     },
       *     {
       *         element: <SchematicViewPage />,
       *         path: '/schematic',
       *     },
       *     {
       *         element: <AnalysisViewPage />,
       *         path: '/analysis',
       *     },
       * ], */
    },
]);

export { router };
