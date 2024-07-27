import { useState, createContext } from 'react';
import { isEmpty as _isEmpty, isNil as _isNil } from 'lodash';

export const SchematicUiContext = createContext();

export default function useSpatialGraphUi() {
    const [uiParams, setSchematicUiParams] = useState({});

    const handleSchematicParams = (newParams, options = {}) => {
        if (_isNil(options) || _isEmpty(options)) {
            setSchematicUiParams((prevParams) => ({
                ...prevParams,
                ...newParams,
            }));
        }

        if (options.resetAll) {
            setSchematicUiParams(newParams);
        }
        return setSchematicUiParams(newParams);
    };

    return { ...uiParams, setSchematicUiParams: handleSchematicParams };
}
