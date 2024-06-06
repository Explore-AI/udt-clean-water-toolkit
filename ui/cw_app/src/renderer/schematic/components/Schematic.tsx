// use this to create the schematic view
import LoadingSpinner from '../../core/components/LoadingSpinner';
import { TRUNKMAIN_QUERY_KEY } from '../queries';
import { isEmpty as _isEmpty } from 'lodash';
import styles from '../css/Schematic.module.css';
import useFetchSchematicData from '../hooks/useFetchSchematic';
import { AssetNode } from './AssetNode';
import { PipeEdgeNode } from './PipeNode';
import ReactFlow, { Controls, Background } from 'reactflow';
import 'reactflow/dist/base.css';
import useElkLayout from '../hooks/useElkLayout';

const nodeTypes = {
    assetNode: AssetNode,
    pipeNode: PipeEdgeNode,
};

function Schematic() {
    const { data, isPending, isSuccess } = useFetchSchematicData([
        TRUNKMAIN_QUERY_KEY,
    ]);
    const { data: layoutData, isPending: isLayoutPending } = useElkLayout(
        data || { nodes: [], edges: [] },
    );

    if (isPending) {
        return <LoadingSpinner />;
    }

    if (_isEmpty(data) && isSuccess) {
        return (
            <div>
                <h1>No data found</h1>
            </div>
        );
    }

    return (
        <>
            <ReactFlow
                nodes={layoutData?.nodes}
                edges={layoutData?.edges}
                nodeTypes={nodeTypes}
                minZoom={0}
                maxZoom={50}
                zoomOnScroll={true}
                fitView={true}
                nodesDraggable={true}
                className={styles.rfContainer}
            >
                {/* <Background /> */}
                <Controls />
            </ReactFlow>
        </>
    );
}

export default Schematic;
