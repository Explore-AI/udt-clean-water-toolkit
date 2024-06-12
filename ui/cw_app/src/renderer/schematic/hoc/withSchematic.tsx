import useNodePopups, { NodePopupContext} from "../hooks/useSchematicPopups";
import React from "react";
import { PageProps } from "../types/types";


const withSchematic = ( PageComponent: React.FC<PageProps> ) => {
    const HOC = (props: PageProps) => {
        const popups = useNodePopups();
        return(
            <NodePopupContext.Provider value={popups}>
                <PageComponent {...props} />
            </NodePopupContext.Provider>
        )
        
    }
    return HOC; 
}

export default withSchematic;