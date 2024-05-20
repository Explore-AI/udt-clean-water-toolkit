import React, { useContext, useState } from 'react';
import { isEmpty as _isEmpty, isNil as _isNil } from 'lodash'

export const MapUiContext = React.createContext();

export default function useMapUi() {
    const [uiParams, setMapUiParams] = useState({});

    const handleMapUiParams = (newParams, options = {}) => {
        if (_isEmpty(newParams) || _isNil(newParams)) {
            return setMapUiParams({});
        }
        return setMapUiParams({ ...uiParams, ...newParams });
    };

    return { uiParams, setMapUiParams: handleMapUiParams };
}
