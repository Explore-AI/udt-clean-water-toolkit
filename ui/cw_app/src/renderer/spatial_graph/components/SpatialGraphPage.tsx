import styles from '../css/spatial-graph-page.module.css';
import SpatialGraph from  './SpatialGraph';
import useFetchJson from '../../core/hooks/useFetchJson';
import useFetchItems from '../../core/hooks/useFetchItems'

const SPATIAL_GRAPH__QUERY_KEY = 'cw_graph/schematic'
const DMA__QUERY_KEY = 'cw_utilities/dma'

const SpatialGraphPage = (props) => {
    const { pageVisibility } = props

    useFetchJson(SPATIAL_GRAPH__QUERY_KEY, { params: {'dma_code': 'ZCHIPO01' }})

    useFetchItems(DMA__QUERY_KEY)

    const mainCss = `${styles.main} ${styles[pageVisibility]}`

    return (
        <div className={mainCss}>
            <SpatialGraph />
        </div>
    );
}

export default SpatialGraphPage



//if (error) content = <div>{'An error has occurred: ' + error.message}</div>;
