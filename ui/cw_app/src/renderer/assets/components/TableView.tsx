import useGetData from '../../core/hooks/useGetData';
import { TRUNK_MAINS } from '../queries';
import LoadingSpinner from '../../core/components/LoadingSpinner';
import { useState } from 'react';
import { Table, ScrollArea } from '@mantine/core';
import { Assets, ApiResponse } from '../types/types';
import styles from '../css/TableView.module.css';
import { Table as AssetsTable } from './Table';

export const TableView = () => {
    const { queryValues } = useGetData(TRUNK_MAINS);
    const { data, isPending } = queryValues;

    if (isPending) {
        return <LoadingSpinner />;
    }
    const { items } = data as ApiResponse;

    const rows = items.map((row: Assets) => (
        <Table.Tr key={row.gid}>
            <Table.Td>{row.gid}</Table.Td>
            <Table.Td>{row.geometry}</Table.Td>
            <Table.Td>{row.modified_at}</Table.Td>
            <Table.Td>{row.created_at}</Table.Td>
            <Table.Td>{row.dmas}</Table.Td>
        </Table.Tr>
    ));

    return (
        <>
            <div className={styles.container}>
                <AssetsTable items={items}/>
            </div>
        </>
    );
};
