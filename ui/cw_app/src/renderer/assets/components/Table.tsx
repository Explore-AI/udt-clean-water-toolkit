import { useMemo, useContext } from 'react';
import {
    MantineReactTable,
    useMantineReactTable,
    type MRT_ColumnDef,
} from 'mantine-react-table';
import { ActionIcon, Tooltip } from '@mantine/core';
import { IconRefresh } from '@tabler/icons-react';
import { Assets, ApiResponse } from '../types/types';
import { TableContext } from '../hooks/useTableUi';
import useGetData from '../../core/hooks/useGetData';
import styles from '../css/Table.module.css'
import { getTableTitle } from '../utils/utils';

export const Table = () => {
    const { selectedKey } = useContext(TableContext);
    const { queryValues } = useGetData(selectedKey);
    const { data, isLoading, isFetching, refetch, isError } = queryValues;
    const label = getTableTitle(selectedKey.split('/')[1]); 


    // abstract the table to display any kind of data from the assets tables found in the psql db
    const columns = useMemo<MRT_ColumnDef<Assets>[]>(
        () => [
            {
                accessorKey: 'gid',
                header: 'GISID',
                mantineTableHeadCellProps: {
                    style: { backgroundColor: '#33658A', color: '#fff' },
                },
            },
            {
                accessorKey: 'geometry',
                header: 'Geometry',
                mantineTableHeadCellProps: {
                    style: { backgroundColor: '#33658A', color: '#fff' },
                },
            },
            {
                accessorKey: 'created_at',
                header: 'Created At',
                mantineTableHeadCellProps: {
                    style: { backgroundColor: '#33658A', color: '#fff' },
                },
            },
            {
                accessorKey: 'modified_at',
                header: 'Modified At',
                mantineTableHeadCellProps: {
                    style: { backgroundColor: '#33658A', color: '#fff' },
                },
            },
            {
                accessorKey: 'dmas',
                header: 'DMAS',
                mantineTableHeadCellProps: {
                    style: { backgroundColor: '#33658A', color: '#fff' },
                },
            },
        ],
        [],
    );

    const { items } = data as ApiResponse ?? []; 
    const assetData = items ? items : []; 

    const table = useMantineReactTable({
        columns,
        data: assetData,
        initialState: { showColumnFilters: true },
        mantineToolbarAlertBannerProps: isError
            ? { color: 'red', children: 'Error loading data' }
            : undefined,
        renderTopToolbarCustomActions: () => (
            <div className={styles.toolbar}> 
                
                <Tooltip label="Refresh Data">
                    <ActionIcon onClick={() => refetch()}>
                        <IconRefresh />
                    </ActionIcon>
                </Tooltip>
                <div className={styles.title}> {label} </div>
            </div>
        ),
        enableRowSelection: true,
        enableColumnOrdering: true,
        enableGlobalFilter: false,
        mantineTableContainerProps: {
            style: { maxHeight: '60vh', width: '100%', border: '#fff' }, //give the table a max height
        }, 
        state: {
            isLoading: isLoading,
            showAlertBanner: isError,
            showProgressBars: isFetching,
        },
    });

    return <MantineReactTable table={table} />;
};
