import 'reactflow/dist/style.css';
import ReactFlow, { Controls } from 'reactflow';
import CircleNode from './CircleNode';
import EdgeNode from './EdgeNode';
import useGetData from '../../core/hooks/useGetData'

const SPATIAL_GRAPH__QUERY_KEY = 'cw_graph/schematic'

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

    const { data } = useGetData(SPATIAL_GRAPH__QUERY_KEY)

    return (
        <ReactFlow
            defaultNodes={data.nodes}
            defaultEdges={data.edges}
            nodeTypes={nodeTypes}
            minZoom={0}
            maxZoom={50}
            fitView={true}
            nodesDraggable={false}
        >
            <Controls />
        </ReactFlow>
    );
};

export default SpatialGraph;
