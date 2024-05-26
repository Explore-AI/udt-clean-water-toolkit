import { useCallback } from 'react'
import ReactFlow, {
    Controls,
    useEdgesState
} from 'reactflow';
import CircleNode from './CircleNode';
import FloatingEdge from './FloatingEdge'
import { createNodesAndEdges } from './utils.js';
//import ButtonEdge from './ButtonEdge';

import 'reactflow/dist/style.css';

const nodeTypes = {
    circle: CircleNode,
    edge_node: CircleNode,
};

const edgeTypes = {
    floating: FloatingEdge,
};


const { nodes: initialNodes, edges: initialEdges } = createNodesAndEdges();


const Schematic = (props) => {

    const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);


    const onConnect = useCallback(
        (params) =>
            setEdges((eds) =>
                addEdge({ ...params, type: 'floating', markerEnd: { type: MarkerType.Arrow } }, eds)
            ),
        [setEdges]
    );

    return (
        <ReactFlow
            nodes={props.nodes}
            edges={props.edges}
            nodeTypes={nodeTypes}
            onConnect={onConnect}
            connectionMode="loose"
            connectionRadius={1}
            minZoom={0}
            maxZoom={50}
            fitView
        >
            <Controls />
        </ReactFlow>
    );
};

export default Schematic;
