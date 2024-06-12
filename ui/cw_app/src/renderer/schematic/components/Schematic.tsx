// use this to create the schematic view
import LoadingSpinner from '../../core/components/LoadingSpinner';
import { TRUNKMAIN_QUERY_KEY } from '../queries';
import { isEmpty as _isEmpty } from 'lodash';
import styles from '../css/Schematic.module.css';
import useFetchSchematicData from '../hooks/useFetchSchematic';
import AssetNode from './AssetNode';
import PipeEdgeNode from './PipeNode';
import ReactFlow, { Controls, Node } from 'reactflow';
import 'reactflow/dist/base.css';
import useElkLayout from '../hooks/useElkLayout';
import { useState } from 'react';
import { AssetPopup } from './AssetPopup';
import useAssetNodePopups from '../hooks/useSchematicPopups';

const nodeTypes = {
    assetNode: AssetNode,
    pipeNode: PipeEdgeNode,
};

const onNodeClick = (event: React.MouseEvent, node: Node, openPopup: any) => {
    console.log(node);
    // toggle popup display
    openPopup(node);
}

function Schematic() {
    const { data, isPending, isSuccess } = useFetchSchematicData([
        TRUNKMAIN_QUERY_KEY,
    ], { limit: 20 });


    const { data: layoutData } = useElkLayout(
        data || { nodes: [], edges: [] },
    );

    const { popups, openPopup, closePopup} = useAssetNodePopups(); 
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
    console.log('List of popups: \n', popups); 

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
                onNodeClick={(event, node) => onNodeClick(event, node, openPopup)}
            >
                { popups.map((nodePopup)=> (
                    <AssetPopup key={nodePopup.id} nodeProps={nodePopup}/>
                ))}
                {/* <Background /> */}
                <Controls />
            </ReactFlow>
        </>
    );
}

export default Schematic;
