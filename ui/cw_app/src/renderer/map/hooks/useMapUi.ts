import React, { useContext, useState } from 'react';

export const MapUiContext = React.createContext();

export default function useMapUi() {
    const [uiParams, setMapUiParams] = useState({});

    const handleMapUiParams = (newParams, options = {}) => {
        if (isEmpty(newParams) || isNil(newParams)) {
            return setMapUiParams({});
        }
        return setUiParams({ ...uiParams, ...newParams });
    };

    return { uiParams, setMapUiParams: handleMapUiParams };
}
