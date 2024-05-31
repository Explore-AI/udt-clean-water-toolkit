import MapPage from '../../map/components/MapPage'
import GraphPage from '../../graph/components/GraphPage'
import AnalysisPage from '../../analysis/components/AnalysisPage'
import SpatialGraphPage from '../../spatial_graph/components/SpatialGraphPage'
import { useLocation } from 'react-router-dom'

const  BaseSinglePage = () => {

    const { pathname } = useLocation()

    const pageVisibility = {
        map: pathname === '/map'? 'inherit': 'none',
        graph: pathname === '/graph'? 'inherit': 'none',
        ['geo-graph']: pathname === '/geo-graph'? 'inherit': 'none',
        schematic: pathname === '/schematic'? 'inherit': 'none',
        analysis: pathname === '/analysis'? 'inherit': 'none',
    }

    return (
        <>
            <MapPage pageVisibility={pageVisibility.map} />
            <GraphPage pageVisibility={pageVisibility.graph} />
            <SpatialGraphPage pageVisibility={pageVisibility['geo-graph']} />
            <AnalysisPage pageVisibility={pageVisibility.analysis} />
        </>
    );
}

export default BaseSinglePage;
