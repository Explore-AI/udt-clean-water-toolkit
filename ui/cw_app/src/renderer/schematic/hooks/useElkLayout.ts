// https://reactflow.dev/examples/layout/elkjs-multiple-handles
import { useEffect } from 'react';
import ELK from 'elkjs/lib/elk.bundled';
import { Node, Edge as PipeEdge, SchematicProps } from '../types/types';
import { useQuery } from '@tanstack/react-query';

const layoutOptions = {
    'elk.algorithm': 'layered',
    'elk.direction': 'RIGHT',
    'elk.layered.spacing.edgeNodeBetweenLayers': '40',
    'elk.spacing.nodeNode': '40',
    'elk.layered.nodePlacement.strategy': 'SIMPLE',
};

const elk = new ELK();

const getNodesLayout = async ({ nodes, edges }: SchematicProps) => {
    
    const graph = {
        id: 'root',
        layoutOptions,
        children: nodes.map((node) => ({
            id: node.id,
            width: 150, // You can adjust width based on your node size
            height: 50, // You can adjust height based on your node size
            properties: {
                label: node.key,
                'org.eclipse.elk.portConstraints': 'FIXED_POS',
            },
        })),
        edges: edges.map((edge) => ({
            id: edge.id,
            sources: [edge.source],
            targets: [edge.target],
        })),
    };

    const graphLayout = await elk.layout(graph);

    
    const nodesLayout = nodes.map((node) => {
        const nodeLayout = graphLayout.children?.find(
            (child) => child.id === node.id,
        );
        return {
            ...node,
            position: { x: nodeLayout?.x ?? 0, y: nodeLayout?.y ?? 0 },
        };
    });

    return {nodes: nodesLayout, edges: edges};
};

export default function useElkLayout(data: SchematicProps) {
    // console.log('Hit the Elk Layout hook')
    const layoutData =  useQuery({
        queryKey: ['nodesLayout', data],
        queryFn: async () => {
            let layoutData = await getNodesLayout(data);
            // console.log('Layout Data returned in the hook: ', layoutData)
            return layoutData;
        },
        enabled: !!data.nodes.length && !!data.edges.length,
    });
    return layoutData;
}
