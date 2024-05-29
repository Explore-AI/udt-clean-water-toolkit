import ReactFlow, {
    Controls
} from 'reactflow';
import CircleNode from './CircleNode';
import EdgeNode from './EdgeNode'

import 'reactflow/dist/style.css';

const nodeTypes = {
    circle: CircleNode,
    edge_node: EdgeNode,
};

const Schematic = (props) => {
    const { nodes, edges } = props

    return (
        <ReactFlow
            defaultNodes={nodes}
            defaultEdges={edges}
            nodeTypes={nodeTypes}
            minZoom={0}
            maxZoom={50}
            fitView={true}        >
            <Controls />
        </ReactFlow>
    );
};

export default Schematic;
