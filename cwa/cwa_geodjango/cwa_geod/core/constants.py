### For storing constants only
### Do not import app objects into this file to avoid circular imports

DEFAULT_SRID = 27700

TRUNK_MAIN__NAME = "trunk_main"

DISTRIBUTION_MAIN__NAME = "distribution_main"

CHAMBER__NAME = "chamber"

HYDRANT__NAME = "hydrant"

LOGGER__NAME = "logger"

NETWORK_METER__NAME = "network_meter"

NETWORK_OPT_VALVE__NAME = "network_opt_valve"

OPERATIONAL_SITE__NAME = "operational_site"

PRESSURE_CONTROL_VALVE__NAME = "pressure_control_valve"

PRESSURE_FITTING__NAME = "pressure_fitting"

PIPE_END__NAME = "pipe_end"

PIPE_JUNCTION__NAME = "pipe_junction"

POINT_ASSET__NAME = "point_asset"

PIPE_ASSETS__CHOICES = [
    (TRUNK_MAIN__NAME, "Trunk Main"),
    (DISTRIBUTION_MAIN__NAME, "Distribution Main"),
]

PIPE_ASSETS__NAMES = [TRUNK_MAIN__NAME, DISTRIBUTION_MAIN__NAME]

ASSET__LABELS = {
    TRUNK_MAIN__NAME: "TrunkMain",
    DISTRIBUTION_MAIN__NAME: "DistributionMain",
    CHAMBER__NAME: "Chamber",
    HYDRANT__NAME: "Hydrant",
    LOGGER__NAME: "Logger",
    NETWORK_METER__NAME: "NetworkMeter",
    NETWORK_OPT_VALVE__NAME: "network_opt_valve",
    OPERATIONAL_SITE__NAME: "OperationalSite",
    PRESSURE_CONTROL_VALVE__NAME: "PressureControlValve",
    PRESSURE_FITTING__NAME: "PressureFitting",
}


GEOS_LINESTRING_TYPES = [1, 5]

GEOS_POINT_TYPES = [0]

UTILITIES = [
    ("thames_water", "Thames Water"),
    ("severn_trent_water", "Severn Trent Water"),
]
