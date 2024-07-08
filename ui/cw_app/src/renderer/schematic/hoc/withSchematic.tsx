import React from 'react';
import { PageProps } from '../../core/types/types';
import useSchematicUi, { SchematicUiContext } from '../hooks/useSchematicUi';

const withSchematic = (PageComponent: React.FC<PageProps>) => {
    const HOC = (props: PageProps) => {

        const schematicUiValues = useSchematicUi();

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

export default withSchematic;
