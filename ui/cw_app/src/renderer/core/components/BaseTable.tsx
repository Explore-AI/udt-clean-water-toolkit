// create a generic Asset Table component that accepts data
import { useMemo } from 'react';
import {
    MantineReactTable,
    useMantineReactTable,
    type MRT_ColumnDef,
} from 'mantine-react-table';
import { ActionIcon, Tooltip } from '@mantine/core';
import { IconRefresh } from '@tabler/icons-react';
import { BaseTableProps, AssetsDataType } from '../types/types';
import styles from '../css/BaseTable.module.css';

export const BaseTable = ({
    data,
    isLoading,
    assetColumns,
    assetName,
    refetch,
    manualPagination,
    rowCount,
    onPaginationChange,
    pagination,
    pageCount,
}: BaseTableProps) => {
    const columns = useMemo<MRT_ColumnDef<AssetsDataType>[]>(
        () => assetColumns,
        [assetColumns],
    );
    

    const table = useMantineReactTable({
        columns,
        data,
        initialState: {
            showColumnFilters: true,
            isLoading: true,
        },
        renderTopToolbarCustomActions: () => (
            <div className={styles.toolbar}>
                <Tooltip label="Refresh Data">
                    <ActionIcon onClick={() => refetch()}>
                        <IconRefresh />
                    </ActionIcon>
                </Tooltip>
                <div className={styles.title}> {assetName} </div>
            </div>
        ),
        enableRowSelection: true,
        enableColumnOrdering: true,
        enableGlobalFilter: false,
        mantineTableProps: { striped: 'even' },
        paginationDisplayMode: 'pages',
        mantineTableHeadCellProps: { className: styles.header },
        mantineTableContainerProps: {
            style: { height: '65vh', width: '100%', border: '#fff' },
        },
        state: {
            isLoading: isLoading,
            pagination: pagination,
        },
        manualPagination: manualPagination,
        rowCount: rowCount,
        pageCount: pageCount,
        onPaginationChange: onPaginationChange,
    });

    return <MantineReactTable table={table} />;
};
