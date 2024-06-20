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
