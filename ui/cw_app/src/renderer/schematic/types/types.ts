export type PageProps = {
    pageVisibility: string;
};

export type Node = {
    id: string;
    key: string;
    type: string;
    position: { x: number; y: number };
    data: any;
};

export type Edge = {
    id: string;
    key: string;
    source: string;
    target: string;
    type: string;
    style: { strokeWidth: string; color: string };
};

export type SchematicProps = {
    nodes: Node[]; 
    edges: Edge[] 
};

