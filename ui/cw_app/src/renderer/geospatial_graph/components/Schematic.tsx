import ReactFlow, { Controls } from 'reactflow';
import CircleNode from './CircleNode';
import EdgeNode from './EdgeNode';

import 'reactflow/dist/style.css';

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

type Props = {
    nodes: Node[];
    edges: Edge[];
};

const Schematic = (props: Props) => {
    const { nodes, edges } = props;

    return (
        <ReactFlow
            defaultNodes={nodes}
            defaultEdges={edges}
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

export default Schematic;
