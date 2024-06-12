// hook that creates and manages the Context for the Node Popups
import { createContext, useState } from 'react';
import { Node } from 'reactflow';
import { Node as AssetNode } from '../types/types';

export const NodePopupContext = createContext();

export default function useAssetNodePopups() {
    const [popups, setPopups] = useState<Node<AssetNode>[]>([]);

    const openPopup = (node: Node) => {
        setPopups([...popups, node]);
    };

    const closePopup = (id: string) => {
        setPopups((prevPopups) =>
            prevPopups.filter((popup) => popup.id !== id),
        );
    };

    return { popups, openPopup, closePopup };
}
