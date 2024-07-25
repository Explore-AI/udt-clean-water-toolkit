import styles from '../css/spatial-graph-page.module.css';
import SpatialGraph from  './SpatialGraph';
import useFetchJson from '../../core/hooks/useFetchJson';
import useFetchItems from '../../core/hooks/useFetchItems'
import { useParams } from 'react-router-dom';

const SPATIAL_GRAPH__QUERY_KEY = 'cw_graph/spatial_graph'
const DMA__QUERY_KEY = 'cw_utilities/dma'

const SpatialGraphPage = (props) => {
    const { pageVisibility } = props

    const { dmas } = useParams()

    let dmaCodes
    if (dmas) {
        dmaCodes = dmas.split('-');
    }

    useFetchJson(SPATIAL_GRAPH__QUERY_KEY, { params: {'dma_codes': dmaCodes }, limit: 7000})

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
