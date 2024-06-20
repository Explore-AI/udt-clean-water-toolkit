const QUERY_PREFIX = 'cw_gis_assets'
export const DIST_MAINS = `${QUERY_PREFIX}/distribution_main`
export const TRUNK_MAINS = `${QUERY_PREFIX}/trunk_main`
export const CHAMBER = `${QUERY_PREFIX}/chamber`
export const HYDRANT = `${QUERY_PREFIX}/hydrant`
export const LOGGER = `${QUERY_PREFIX}/logger`
export const NETWORK_METER = `${QUERY_PREFIX}/network_meter`
export const NETWORK_OPT_VALVE = `${QUERY_PREFIX}/network_opt_valve`
export const OPERATIONAL_SITE = `${QUERY_PREFIX}/operational_site`
export const PRESSURE_CONTROL_VALVE = `${QUERY_PREFIX}/pressure_control_valve`
export const PRESSURE_FITTING = `${QUERY_PREFIX}/pressure_fitting`

type tableType = {
    [key: string]: string;
}
const tableKeys = {
        trunk_main: TRUNK_MAINS,
        distribution_main: DIST_MAINS,
        chamber: CHAMBER,
        hydrant: HYDRANT,
        logger: LOGGER,
        network_meter: NETWORK_METER,
        network_opt_valve: NETWORK_OPT_VALVE,
        operational_site: OPERATIONAL_SITE,
        pressure_control_valve: PRESSURE_CONTROL_VALVE,
        pressure_fitting: PRESSURE_FITTING,
} as tableType

export const getKey = (key: string) => tableKeys[key] || key; 