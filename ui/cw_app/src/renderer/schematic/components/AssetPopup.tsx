// create a popup for the asset node's properties
import { Node } from "reactflow";
import { Node as AssetNodeType} from "../types/types";
import { AssetPopupProps } from "../types/types";


export const AssetPopup: React.FC<AssetPopupProps> = ({nodeProps}) => {
    
    console.log('Position of our Node in the react flow diagram!', nodeProps.position); 

    return (
        <>
            <div>
                <h1> Asset Popup Here!</h1>
            </div>
        </>
    );
};
