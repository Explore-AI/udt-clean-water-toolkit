import 'reactflow/dist/style.css';
import styles from '../css/spatial-graph.module.css'
import ReactFlow, { Controls } from 'reactflow';
import CircleNode from './CircleNode';
import EdgeNode from './EdgeNode';
import LoadingSpinner from '../../core/components/LoadingSpinner';
import useGetData from '../../core/hooks/useGetData'
import useGetItems from '../../core/hooks/useGetItems'
import MultiSelectField from '../../core/components/MultiSelectField'
import { useNavigate } from 'react-router-dom';
//import useFilterParams from '../../core/hooks/useFilterParams'

const SPATIAL_GRAPH__QUERY_KEY = 'cw_graph/spatial_graph'
const DMA__QUERY_KEY = 'cw_utilities/dma'

const nodeTypes = {
    circle: CircleNode,
    edge_node: EdgeNode,
};
type Node = {
    id: string;
    key: string;
    type: string;
    position: { x: number; y: number };
    data: any;
};

type Edge = {
    id: string;
    key: string;
    source: string;
    target: string;
    type: string;
    style: { strokeWidth: string; color: string };
};

const SpatialGraph = () => {

    const navigate = useNavigate();

    const { queryValues } = useGetData(SPATIAL_GRAPH__QUERY_KEY)
    const { data, isLoading } = queryValues;

    const { items, setFilterParams } = useGetItems(DMA__QUERY_KEY)

    if (isLoading)  {
        return <LoadingSpinner/>
    }

    const onSearchChange = (value) => {
        setFilterParams(DMA__QUERY_KEY, { search: value })
    }

    const onFilterByDmas = (options) => {
        navigate(`/spatial-graph/${options.join("-")}`);
    }


    return (
        <>
            <div className={styles['search_box']}>
                <MultiSelectField
                    labelName="code"
                    clearable={true}
                    onEnter={onFilterByDmas}
                    onSearchChange={onSearchChange}
                    placeholder="Search by DMA"
                    searchable={true}
                    data={items} />
            </div>
            <div className={styles.rflow}>
                <ReactFlow
                    defaultNodes={data?.nodes}
                    defaultEdges={data?.edges}
                    nodeTypes={nodeTypes}
                    minZoom={0}
                    maxZoom={50}
                    fitView={true}
                    className={styles.rfContainer}
                    nodesDraggable={false}
                >
                    <Controls />
                </ReactFlow>
            </div>
        </>
    );
};

export default SpatialGraph;
