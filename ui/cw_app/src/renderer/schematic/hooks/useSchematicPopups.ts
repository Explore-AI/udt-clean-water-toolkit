// hook that creates and manages the UI changes for the Node Popups in Schematic View 
import { createContext, useState } from 'react';
import { Node } from 'reactflow';
import { Node as AssetNode } from '../types/types';
// @ts-ignore
export const NodePopupContext = createContext();

export default function useAssetNodePopups() {
    const [popups, setPopups] = useState<Node<AssetNode>[]>([]);

    const openPopup = (node: Node<AssetNode>) => {
        setPopups([...popups, node]);
    };

    const closePopup = (id: string) => {
        setPopups((prevPopups) =>
            prevPopups.filter((popup) => popup.id !== id),
        );
    };

    return { popups, openPopup, closePopup };
}
