import { useState, createContext } from 'react';
import { isEmpty as _isEmpty, isNil as _isNil } from 'lodash';

export const SchematicUiContext = createContext();

export default function useSchematicUi() {
    const [uiParams, setSchematicUiParams] = useState({});

    const handleSchematicParams = (newParams, options = {}) => {
        if (_isNil(options) || _isEmpty(options)) {
            setSchematicUiParams(newParams);
        }

        if (options.keepCurrent) {
            setSchematicUiParams((prevParams) => ({
                ...prevParams,
                ...newParams,
            }));
        }
        return setSchematicUiParams(newParams);
    };
    return { uiParams, setSchematicUiParams: handleSchematicParams };
}
