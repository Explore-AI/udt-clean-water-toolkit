// create a generic Asset Table component that accepts data
import { useMemo } from 'react';
import {
    MantineReactTable,
    useMantineReactTable,
    type MRT_ColumnDef,
} from 'mantine-react-table';
import { ActionIcon, Tooltip } from '@mantine/core';
import { IconRefresh } from '@tabler/icons-react';
import { AssetTableProps, AssetsDataType } from '../types/types';
import styles from '../css/AssetTable.module.css'

export const AssetTable = ({
    data,
    isLoading, 
    assetColumns,
    assetName,
    refetch
}: AssetTableProps) => {
    const columns = useMemo<MRT_ColumnDef<AssetsDataType>[]>(
        () => assetColumns,
        [],
    );

    const table = useMantineReactTable({
        columns,
        data,
        initialState: { showColumnFilters: true, isLoading: true },
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
        mantineTableContainerProps: {
            style: { maxHeight: '60vh', width: '100%', border: '#fff' },
        },
        state: {
            isLoading: isLoading, 
        }
    });

    return <MantineReactTable table={table} />;
};
