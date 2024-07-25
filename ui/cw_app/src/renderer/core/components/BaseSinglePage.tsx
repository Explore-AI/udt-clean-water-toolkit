import MapPage from '../../map/components/MapPage'
import GraphPage from '../../graph/components/GraphPage'
import ExplorerPage from '../../explorer/components/ExplorerPage'
import AnalysisPage from '../../analysis/components/AnalysisPage'
import SpatialGraphPage from '../../spatial_graph/components/SpatialGraphPage'
import SchematicPage from '../../schematic/components/SchematicPage';
import AssetsPage from '../../assets/components/AssetsPage';
import { useLocation } from 'react-router-dom'
import { startsWith as _startsWith } from 'lodash'

const BaseSinglePage = () => {
    const { pathname } = useLocation();

    const pageVisibility = {
        map: _startsWith(pathname,'/map') ? 'visible': 'hidden',
        graph: _startsWith(pathname,'/graph') ? 'visible': 'hidden',
        explorer: _startsWith(pathname,'/explorer') ? 'visible': 'hidden',
        spatialGraph: _startsWith(pathname, '/spatial-graph') ? 'visible': 'hidden',
        schematic: _startsWith(pathname, '/schematic') ? 'visible': 'hidden',
        analysis: _startsWith(pathname, '/analysis') ? 'visible': 'hidden',
        assets: _startsWith(pathname, '/assets') ? 'visible': 'hidden',
    }

    return (
        <>
            {/* <MapPage pageVisibility={pageVisibility.map} /> */}
            {/* <GraphPage pageVisibility={pageVisibility.graph} /> */}
            {/* <ExplorerPage pageVisibility={pageVisibility.explorer} /> */}
            {/* <SpatialGraphPage pageVisibility={pageVisibility.spatialGraph} /> */}
            <SchematicPage pageVisibility={pageVisibility.schematic} />
            {/* <AnalysisPage pageVisibility={pageVisibility.analysis} /> */}
            {/* <AssetsPage pageVisibility={pageVisibility.assets} /> */}
        </>
    );
};

export default BaseSinglePage;
