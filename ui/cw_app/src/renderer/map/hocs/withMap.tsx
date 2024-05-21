import useMapUi, { MapUiContext } from '../hooks/useMapUi';
import useMapLayers, { MapLayerContext } from '../hooks/useMapLayers';

const withMap = (PageComponent) => {
    const HOC = (props) => {
        const mapLayerValues = useMapLayers();
        const { uiParams, setMapUiParams } = useMapUi();

        return (
            <MapLayerContext.Provider value={mapLayerValues}>
                <MapUiContext.Provider value={{ uiParams, setMapUiParams }}>
                    <PageComponent {...props} />
                </MapUiContext.Provider>
            </MapLayerContext.Provider>
        );
    };

    return HOC;
};

export default withMap;
