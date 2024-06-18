import useNodePopups, { NodePopupContext } from '../hooks/useSchematicPopups';
import React from 'react';
import { PageProps } from '../types/types';
import useSchematicUi, { SchematicUiContext } from '../hooks/useSchematicUi';

const withSchematic = (PageComponent: React.FC<PageProps>) => {
    const HOC = (props: PageProps) => {
        const popups = useNodePopups();
        const { uiParams, setSchematicUiParams } = useSchematicUi();
        return (
            <NodePopupContext.Provider value={popups}>
                <SchematicUiContext.Provider
                    value={{ uiParams, setSchematicUiParams }}
                >
                    <PageComponent {...props} />
                </SchematicUiContext.Provider>
            </NodePopupContext.Provider>
        );
    };
    return HOC;
};

export default withSchematic;
