import MapPage from '../../map/components/MapPage'
import GraphPage from '../../graph/components/GraphPage'
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
        spatialGraph: _startsWith(pathname, '/spatial-graph') ? 'visible': 'hidden',
        schematic: _startsWith(pathname, '/schematic') ? 'visible': 'hidden',
        analysis: _startsWith(pathname, '/analysis') ? 'visible': 'hidden',
        assets: _startsWith(pathname, '/assets') ? 'visible': 'hidden',
    }

    return (
        <>
            <MapPage pageVisibility={pageVisibility.map} />
            {/* <GraphPage pageVisibility={pageVisibility.graph} />
            <SpatialGraphPage pageVisibility={pageVisibility.spatialGraph} />
            <AnalysisPage pageVisibility={pageVisibility.analysis} /> */}
            <SchematicPage pageVisibility={pageVisibility.schematic} />
            {/* <AssetsPage pageVisibility={pageVisibility.assets} /> */}
        </>
    );
};

export default BaseSinglePage;
