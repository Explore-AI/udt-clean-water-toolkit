import React from 'react';
import { PageProps } from '../../core/types/types';
import useTableUi, { TableContext } from '../hooks/useTableUi';
import { TRUNK_MAINS } from '../queries';

const withTable = (PageComponent: React.FC<PageProps>) => {
    const WithTable = (props: PageProps) => {
        const tableUi = useTableUi({
            selectedKey: TRUNK_MAINS,
        });

        return (
            <TableContext.Provider value={tableUi}>
                <PageComponent {...props} />
            </TableContext.Provider>
        );
    };

    return WithTable;
};

export default withTable;
