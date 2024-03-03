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

PIPE_ASSETS__NAMES = [
    (TRUNK_MAIN__NAME, "Trunk Main"),
    (DISTRIBUTION_MAIN__NAME, "Distribution Main"),
]

POINT_ASSETS__NAMES = [(), ()]

GEOS_LINESTRING_TYPES = [1, 5]

UTILITIES = [
    ("THAMES WATER", "thames_water"),
    ("SEVERN TRENT WATER", "severn_trent_water"),
]
