import styles from '../css/spatial-graph-page.module.css';
import SpatialGraph from  './SpatialGraph';
import useFetchJson from '../../core/hooks/useFetchJson';

const SPATIAL_GRAPH__QUERY_KEY = 'cw_graph/schematic'

const SpatialGraphPage = (props) => {
    const { pageVisibility } = props

    useFetchJson(SPATIAL_GRAPH__QUERY_KEY, { params: {'dma_code': 'ZCHIPO01' }})

    const mainCss = `${styles.pageContainer} ${pageVisibility}`

    return (
        <div className={mainCss}>
            <SpatialGraph />
        </div>
    );
}

export default SpatialGraphPage



//if (error) content = <div>{'An error has occurred: ' + error.message}</div>;
