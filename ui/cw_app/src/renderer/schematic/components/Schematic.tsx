// use this to create the schematic view
import 'reactflow/dist/base.css';
import { useContext } from 'react'
import LoadingSpinner from '../../core/components/LoadingSpinner';
import styles from '../css/Schematic.module.css';
import AssetNode from './AssetNode';
import PipeEdgeNode from './PipeNode';
import ReactFlow, { Controls, Node } from 'reactflow';
import useElkLayout from '../hooks/useElkLayout';
import useGetData from '../../core/hooks/useGetData';
import { SchematicUiContext } from '../hooks/useSchematicUi'
import { SchematicProps } from '../types/types';
import { TRUNKMAIN_QUERY_KEY } from '../queries';
import { isEmpty as _isEmpty, union as _union } from 'lodash';

const nodeTypes = {
    assetNode: AssetNode,
    pipeNode: PipeEdgeNode,
};

function Schematic() {
    const { queryValues } = useGetData(TRUNKMAIN_QUERY_KEY);
    const { data, isPending, isSuccess } = queryValues
    const { data: layoutData } = useElkLayout(data as SchematicProps || { nodes: [], edges: [] });

    const { nodePopupIds, setSchematicUiParams } = useContext(SchematicUiContext)

    const onNodeClick = (
        e: React.MouseEvent,
        node: Node,
    ) => {
        setSchematicUiParams({ nodePopupIds: _union(nodePopupIds || [], [node.id])});
    };

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
                onNodeClick={onNodeClick}
            >

                <Controls />
            </ReactFlow>
        </>
    );
}

export default Schematic;
