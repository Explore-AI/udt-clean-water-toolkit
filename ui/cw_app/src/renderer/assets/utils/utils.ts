type keyType = {
    [key: string]: string;
};
const keys = {
    trunk_main: 'TRUNK MAINS',
    distribution_main: 'DISTRIBUTION MAINS',
    chamber: 'CHAMBERS',
    hydrant: 'HYDRANTS',
    logger: 'LOGGERS',
    network_meter: 'NETWORK METERS',
    network_opt_valve: 'NETWORK OPT VALVES',
    operational_site: 'OPERATIONAL SITES',
    pressure_control_valve: 'PRESSURE CONTROL VALVES',
    pressure_fitting: 'PRESSURE FITTINGS',
} as keyType; 

export const getTableTitle = (key: string) => {
    return keys[key]; 
};


export const defaultAssetColumns = [
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
]