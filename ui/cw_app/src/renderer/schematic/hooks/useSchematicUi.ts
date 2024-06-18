import { useState, createContext } from 'react'; 
import { isEmpty as _isEmpty, isNil as _isNil } from 'lodash';

export const SchematicUiContext = createContext(); 

export default function useSchematicUi(){
    const [selectedNode, setSelectedNode] = useState(null);
    const [popupOpen, setPopupOpen] = useState(false);

    const handleNodeClick = (node) => {
        setSelectedNode(node);
        setPopupOpen(true);
    };

    const handlePopupClose = () => {
        setPopupOpen(false);
        setSelectedNode(null);
    };

    return {
        selectedNode,
        popupOpen,
        handleNodeClick,
        handlePopupClose,
    };

}