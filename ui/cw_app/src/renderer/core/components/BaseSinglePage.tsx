import MapPage from '../../map/components/MapPage'
import GraphPage from '../../graph/components/GraphPage'
import AnalysisPage from '../../analysis/components/AnalysisPage'
import SpatialGraphPage from '../../spatial_graph/components/SpatialGraphPage'
import SchematicPage from '../../schematic/components/SchematicPage'
import { useLocation } from 'react-router-dom'

const  BaseSinglePage = () => {

    const { pathname } = useLocation()

    const pageVisibility = {
        map: pathname === '/map'? 'visible': 'hidden',
        graph: pathname === '/graph'? 'visible': 'hidden',
        ['geo-graph']: pathname === '/geo-graph'? 'visible': 'hidden',
        schematic: pathname === '/schematic'? 'visible': 'hidden',
        analysis: pathname === '/analysis'? 'visible': 'hidden',
    }

    return (
        <>
             <MapPage pageVisibility={pageVisibility.map} />
            {/*<GraphPage pageVisibility={pageVisibility.graph} />
            <SpatialGraphPage pageVisibility={pageVisibility['geo-graph']} />
            <AnalysisPage pageVisibility={pageVisibility.analysis} /> */}
            <SchematicPage pageVisibility={pageVisibility.schematic} /> 
        </>
    );
}

export default BaseSinglePage;
