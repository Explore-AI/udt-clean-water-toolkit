import { memo, useMemo } from 'react';
import {
    MantineReactTable,
    useMantineReactTable,
    type MRT_ColumnDef,
} from 'mantine-react-table';
import { Assets, ApiResponse } from '../types/types';

export const Table = ({ items }: ApiResponse) => {
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

    // pass table options to useMantineReactTable
    const table = useMantineReactTable({
        columns,
        data: items,
        enableRowSelection: true,
        enableColumnOrdering: true,
        enableGlobalFilter: false,
    });

    return <MantineReactTable table={table} />;
};
