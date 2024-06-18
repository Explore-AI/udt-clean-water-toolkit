// use this to create the schematic view
import LoadingSpinner from '../../core/components/LoadingSpinner';
import { TRUNKMAIN_QUERY_KEY } from '../queries';
import { isEmpty as _isEmpty } from 'lodash';
import styles from '../css/Schematic.module.css';
import AssetNode from './AssetNode';
import PipeEdgeNode from './PipeNode';
import ReactFlow, { Controls, Node } from 'reactflow';
import 'reactflow/dist/base.css';
import useElkLayout from '../hooks/useElkLayout';
import { AssetPopup } from './AssetPopup';
import useAssetNodePopups from '../hooks/useSchematicPopups';
import useGetData from '../../core/hooks/useGetData';
import { SchematicProps } from '../types/types';

const nodeTypes = {
    assetNode: AssetNode,
    pipeNode: PipeEdgeNode,
};

const handleNodeClick = (
    event: React.MouseEvent,
    node: Node,
    openPopup: any,
) => {
    openPopup(node);
};

function Schematic() {
    const { queryValues } = useGetData(TRUNKMAIN_QUERY_KEY);
    const { data, isPending, isSuccess } = queryValues
    const { data: layoutData } = useElkLayout(data as SchematicProps || { nodes: [], edges: [] });

    const { popups, openPopup, closePopup } = useAssetNodePopups();

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
                onNodeClick={(event, node) =>
                    handleNodeClick(event, node, openPopup)
                }
            >
                
                <Controls />
            </ReactFlow>
            {popups.map((nodePopup) => (
                    <AssetPopup
                        key={nodePopup.id}
                        nodeProps={nodePopup}
                        onClose={() => closePopup(nodePopup.id)}
                    />
                ))}
        </>
    );
}

export default Schematic;
