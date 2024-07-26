import React from 'react';
import { PageProps } from '../../core/types/types';
import useSpatialGraphUi, { SchematicUiContext } from '../hooks/useSpatialGraphUi';

const withSpatialGraph = (PageComponent: React.FC<PageProps>) => {
    const HOC = (props: PageProps) => {

        const schematicUiValues = useSpatialGraphUi();

        return (
            <SchematicUiContext.Provider
                value={ schematicUiValues }
            >
                <PageComponent { ...props } />
            </SchematicUiContext.Provider>
        );
    };
    return HOC;
};

export default withSpatialGraph;
