### For storing constants only
### Do not import app objects into this file to avoid circular imports

DEFAULT_SRID = 27700

TRUNK_MAIN__NAME = "trunk_main"

DISTRIBUTION_MAIN__NAME = "distribution_main"

CHAMBER__NAME = "chamber"

HYDRANT__NAME = "hydrant"

LOGGER__NAME = "logger"

NETWORK_METER_NAME = "network_meter"

NETWORK_OPT_VALVE_NAME = "network_opt_valve"

OPERATIONAL_SITE_NAME = "operational_site"

PRESSURE_CONTROL_VALVE_NAME = "pressure_control_valve"

PRESSURE_FITTING_NAME = "pressure_fitting"

PIPE_END__NAME = "pipe_end"

POINT_ASSET__NAME = "point_asset"

PIPE_ASSETS__NAMES = [
    (TRUNK_MAIN__NAME, "Trunk Main"),
    (DISTRIBUTION_MAIN__NAME, "Distribution Main"),
]

POINT_ASSETS__NAMES = [(), ()]

GEOS_LINESTRING_TYPES = [1, 5]

GEOS_POINT_TYPES = [0]

UTILITIES = [
    ("thames_water", "Thames Water"),
    ("severn_trent_water", "Severn Trent Water"),
]
