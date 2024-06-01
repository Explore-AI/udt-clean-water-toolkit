import styles from '../css/SchematicPage.module.css';
import Schematic from './Schematic';
import LoadingSpinner from '../../core/components/LoadingSpinner';
import useFetchJson from '../../core/hooks/useFetchJson';
import { isEmpty } from 'lodash';

const SPATIAL_GRAPH__QUERY_KEY = 'cw_graph/schematic'

const SpatialGraphPage = (props) => {
    const { pageVisibility } = props

    const { isPending, data } = useFetchJson(SPATIAL_GRAPH__QUERY_KEY, { params: {'dma_code': 'ZCHIPO01' }})

    if (isEmpty(data) && isPending)  {
        return <LoadingSpinner/>
    }

    return (
        <div className={styles.pageContainer} style={{ display: pageVisibility }}>
            <Schematic nodes={data.nodes} edges={data.edges}/>
        </div>
    );
}

export default SpatialGraphPage



//if (error) content = <div>{'An error has occurred: ' + error.message}</div>;
