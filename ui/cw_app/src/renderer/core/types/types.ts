import {
    QueryObserverResult,
    UseQueryResult,
    RefetchOptions,
} from '@tanstack/react-query';
import React from 'react';
import { type MRT_ColumnDef } from 'mantine-react-table';

export type PageProps = {
    pageVisibility: string;
};

type AssetColumnType = {
    accessorKey: string;
    header: string;
    mantineTableHeadCellProps: React.CSSProperties;
};

export type AssetsDataType = {
    gid: number;
    geometry: string;
    dmas: number[];
    modified_at: string;
    created_at: string;
    geometry_4326?: string;
};

export type AssetTableProps = {
    data: AssetsDataType[];
    isLoading: boolean;
    assetColumns: MRT_ColumnDef<AssetsDataType>[];
    assetName?: string;
    refetch: (
        options?: RefetchOptions | undefined,
    ) => Promise<QueryObserverResult<unknown, Error>>;
};
