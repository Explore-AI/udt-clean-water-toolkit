export type PageProps = {
    pageVisibility: string;
};
export interface AssetProperties  {
    asset_gids?: number[]; 
    asset_names?: string[]; 
    coords_27700?: number[]; 
    dmas?: string; 
    node_key?: string; 
    node_types?: string[]; 
    utility?: string; 
}

export type Node = {
    id: string;
    key: string;
    type: string;
    position: { x: number; y: number };
    properties?: AssetProperties; 
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


export type AssetNode = {
    id: string; 
    type: string; 
    data: Node; 
}
