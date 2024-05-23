import React, { useCallback } from 'react';
import ReactFlow, {
    MiniMap,
    Controls,
    Background,
} from 'reactflow';
import CircleNode from './CircleNode';
//import ButtonEdge from './ButtonEdge';

import 'reactflow/dist/style.css';
import './overview.css';

const nodeTypes = {
    circle: CircleNode,
};

const nodeClassName = (node) => node.type;

const Schematic = (props) => {

    console.log(props.nodes, "qqq")
    console.log(props.edges, "qqq")

    return (
        <ReactFlow
            nodes={props.nodes}
            edges={props.edges}
            nodeTypes={nodeTypes}
            minZoom={0}
            maxZoom={20}
            fitView
        >
            <MiniMap zoomable pannable nodeClassName={nodeClassName} />
            <Controls />
        </ReactFlow>
    );
};

export default Schematic;
