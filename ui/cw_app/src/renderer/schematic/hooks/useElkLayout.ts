// base implementation taken from: https://reactflow.dev/examples/layout/elkjs-multiple-handles
// modified to fit use case 
import ELK from 'elkjs/lib/elk.bundled';
import { SchematicProps } from '../types/types';
import { useQuery } from '@tanstack/react-query';

const layoutOptions = {
    'elk.algorithm': 'layered',
    'elk.direction': 'RIGHT',
    'elk.layered.spacing.edgeNodeBetweenLayers': '80',
    'elk.spacing.nodeNode': '80',
    'elk.layered.nodePlacement.strategy': 'SIMPLE',
};

const elk = new ELK();

const getNodesLayout = async ({ nodes, edges }: SchematicProps) => {
    
    const graph = {
        id: 'root',
        layoutOptions,
        children: nodes.map((node) => ({
            id: node.id,
            width: 250, 
            height: 90, 
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
            data: {...node},
            position: { x: nodeLayout?.x ?? 0, y: nodeLayout?.y ?? 0 },

        };
    });
    return {nodes: nodesLayout, edges: edges};
};

export default function useElkLayout(data: SchematicProps) {
    const layoutData =  useQuery({
        queryKey: ['nodesLayout', data],
        queryFn: async () => {
            let layoutData = await getNodesLayout(data);
            return layoutData;
        },
        // function will only render if nodes, and edges data is available
        // for more on dependent queries: 
        // https://tanstack.com/query/latest/docs/framework/react/guides/dependent-queries
        enabled: (data.nodes.length > 0 && data.edges.length > 0),
    });
    return layoutData;
}
