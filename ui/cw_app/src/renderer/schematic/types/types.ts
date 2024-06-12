import React from "react";
import { Node as FlowNode } from "reactflow";

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


export type IconKeys = 'network_opt_valve' | 'network_meter' | 'hydrant' | 'pressure_control_valve' | 'sres' | 'logger' | 'default' | 'chambers' | string;

type IconValues = React.JSX.Element; 

export type Icons = {
    [key: string]: IconValues;
}

export type AssetPopupProps = {
    nodeProps: FlowNode<Node>; 
}