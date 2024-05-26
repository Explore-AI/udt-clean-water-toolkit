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


const Schematic = (props) => {
    console.log(props.nodes)
    console.log(props.edges)

    return (
        <ReactFlow
            defaultNodes={props.nodes}
            defaultEdges={props.edges}
            nodeTypes={nodeTypes}
            connectionRadius={1}
            connectionMode="loose"
            minZoom={0}
            maxZoom={50}
            fitView
        >
            <Controls />
        </ReactFlow>
    );
};

export default Schematic;
