// create a custom hook for managing the url parameters of the Table component 
import { useState, createContext } from "react";
import { isEmpty as _isEmpty, isNil as _isNil} from "lodash";

export const TableContext = createContext(); 

export default function useTableUi(initialParams = {}) {
    const [ uiParams, setTableUiParams] = useState(initialParams); 
    
    const handleTableParams = (newParams:any, options={}) => {
        if(_isNil(options) || _isEmpty(options)){
            setTableUiParams((prevParams) => ({
                ...prevParams,
                ...newParams
            }))
        }

        if (options.resetAll){
            setTableUiParams(newParams); 
        }
        return setTableUiParams(newParams); 

    }
    return { ...uiParams, setTableUiParams: handleTableParams }; 
}

