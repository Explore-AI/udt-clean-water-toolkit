import React, { useCallback } from 'react';
import ReactFlow, {
    addEdge,
    MiniMap,
    Controls,
    Background,
    useNodesState,
    useEdgesState,
} from 'reactflow';

import {
    nodes as initialNodes,
    edges as initialEdges,
} from './initial-elements';
/* import AnnotationNode from './AnnotationNode';
 * import ToolbarNode from './ToolbarNode';
 * import ResizerNode from './ResizerNode'; */
import CircleNode from './CircleNode';
/* import TextNode from './TextNode'; */
import ButtonEdge from './ButtonEdge';

import 'reactflow/dist/style.css';
import './overview.css';

const nodeTypes = {
    circle: CircleNode,
};

const edgeTypes = {
    button: ButtonEdge,
};

const nodeClassName = (node) => node.type;

const Schematic = (props) => {
    const [nodes, setNodes, onNodesChange] = useNodesState(props.nodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(props.edges);

    const onConnect = useCallback(
        (params) => setEdges((eds) => addEdge(params, eds)),
        [],
    );

    console.log(nodes, "qqq")

    return (
        <ReactFlow
            nodes={nodes}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            fitView
            attributionPosition="top-right"
            nodeTypes={nodeTypes}
            className="overview"
            minZoom={0}
            maxZoom={20}
        >
            <MiniMap zoomable pannable nodeClassName={nodeClassName} />
            <Controls />
            <Background />
        </ReactFlow>
    );
};

export default Schematic;
