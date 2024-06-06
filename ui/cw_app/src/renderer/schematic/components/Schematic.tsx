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
import ELK from 'elkjs/lib/elk.bundled';
import { useEffect, useState } from 'react';
import { SchematicProps } from '../types/types';



const nodeTypes = {
    assetNode: AssetNode,
    pipeNode: PipeEdgeNode,
};


function Schematic() {
    const { data, isPending, isSuccess } = useFetchSchematicData([
        TRUNKMAIN_QUERY_KEY,
    ]);
    const [layoutData, setLayoutData] = useState({});

    useEffect(() => {
        if (data) {
            const elk = new ELK();
            const graph = {
                id: 'root',
                layoutOptions: {
                    'elk.algorithm': 'layered',
                    'elk.layered.spacing.nodeNodeBetweenLayers': '100',
                    'elk.spacing.nodeNode': '100',
                    'elk.layered.nodePlacement.strategy': 'SIMPLE',
                    'elk.direction': 'RIGHT',
                },
                children: data.nodes.map(node => ({
                    id: node.id,
                    width: 100, // You can adjust width based on your node size
                    height: 50, // You can adjust height based on your node size

                })),
                edges: data.edges.map(edge => ({
                    id: edge.id,
                    sources: [edge.source],
                    targets: [edge.target],
                })),
            };

            elk.layout(graph).then(layout => {
                const nodes = layout.children?.map(node => ({
                    ...data.nodes.find(n => n.id === node.id),
                    position: { x: node.x, y: node.y },
                }));
                const edges = layout.edges?.map(edge => ({
                    ...data.edges.find(e => e.id === edge.id),
                }));
                setLayoutData({ nodes, edges });
            });
        }
    }, [data]);

    if (isPending) return <LoadingSpinner />;

    if (_isEmpty(data) && isSuccess) {
        return (
            <div>
                <h1>No data found</h1>
            </div>
        );
    }
    console.log(layoutData)
    return (
        <>
            <ReactFlow
                nodes={layoutData.nodes}
                edges={layoutData.edges}
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
