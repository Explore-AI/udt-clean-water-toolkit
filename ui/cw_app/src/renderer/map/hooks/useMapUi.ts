import { useState, createContext } from 'react';
import { isEmpty as _isEmpty, isNil as _isNil } from 'lodash';

export const MapUiContext = createContext();

export default function useMapUi() {
    const [uiParams, setMapUiParams] = useState({});

    const handleMapUiParams = (newParams, options = {}) => {
        if (_isEmpty(newParams) || _isNil(newParams)) {
            return setMapUiParams({});
        }

        if (options.keepCurrent) {
            return setMapUiParams({ ...uiParams, ...newParams });
        }

        return setMapUiParams(newParams);
    };

    return { uiParams, setMapUiParams: handleMapUiParams };
}
