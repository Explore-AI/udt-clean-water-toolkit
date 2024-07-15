import React from 'react';
import { PageProps } from '../../core/types/types';
import useTableUi, { TableContext } from '../hooks/useTableUi';

const withAssets = (PageComponent: React.FC<PageProps>) => {
    const WithAssets = (props: PageProps) => {
        const tableUi = useTableUi();

        return (
            <TableContext.Provider value={tableUi}>
                <PageComponent {...props} />
            </TableContext.Provider>
        );
    };

    return WithAssets;
};

export default withAssets;
