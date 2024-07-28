### For storing constants only
### Do not import app objects into this file to avoid circular imports

DEFAULT_SRID = 27700

PIPE_MAIN__NAME = "pipe_main"

CHAMBER__NAME = "chamber"

HYDRANT__NAME = "hydrant"

LOGGER__NAME = "logger"

NETWORK_METER__NAME = "network_meter"

CONNECTION_METER__NAME = "connection_meter"

CONSUMPTION_METER__NAME = "consumption_meter"

NETWORK_OPT_VALVE__NAME = "network_opt_valve"

OPERATIONAL_SITE__NAME = "operational_site"

PRESSURE_CONTROL_VALVE__NAME = "pressure_control_valve"

PRESSURE_FITTING__NAME = "pressure_fitting"

PIPE_END__NAME = "pipe_end"

PIPE_JUNCTION__NAME = "pipe_junction"

POINT_ASSET__NAME = "point_asset"

ISOLATION_VALVE__NAME = "isolation_valve"

BULK_METER__NAME = "bulk_meter"

BOREHOLE__NAME = "boreholes"

NON_RETURN_VALVE__NAME = "nonreturnvalve"

PORTABLE_WATER_STORAGE__NAME = "potable_water_storage"

REGULATOR__NAME = "regulator"

REVENUE_METER__NAME = "revenue_meter"

WATER_FACILITY_CONNECTION__NAME = "waterfacilityconnection"

WATER_PIPE_CONNECTION__NAME = "waterpipeconnection"

WATER_PUMPING_FACILITY__NAME = "water_pumping_facility"

WATER_TREATMENT_WORK__NAME = "water_treatment_work"

PIPE_ASSETS__CHOICES = [
    (PIPE_MAIN__NAME, "Pipe Main"),
]

GEOS_LINESTRING_TYPES = [1, 5]

GEOS_POINT_TYPES = [0]

UTILITIES = [
    ("thames_water", "Thames Water"),
    ("severn_trent_water", "Severn Trent Water"),
]

# PIPE_MATERIALS = {"ductile_iron":"DI","cast_iron":"CI"}


# CI	Cast Iron
# PVC	Poly Vinyl Chloride
# ST	Steel
# WOOD	Wood
# UNK	Unknown
# OTH	Other
# GS	Galvanized Steel
# CL	Clay
# AC	Asbestos Cement
# AK	Alkathene
# APC	Alloyed Polyvinyl Chloride
# BPC	Biaxial Polyvinyl Chloride
# BP	Barrier Pipe(Coated Aluminium)
# BR	Brick
# CR	Ceramic
# CN	Concrete
# CP	Copper
# CC	Coated Copper
# FG	Fibreglass
# GI	Galvanised Iron
# GRP	Glass Reinforced Plastic
# LD	Lead
# MOPC	Molecular Orientated Polyvinyl Chloride
# POL	Polyethylene (Black Poly)
# SI	Spun Iron
# CS	Coated Steel
# UPC	Unplasticised Polyvinyl Chloride
# HPPE	PE100 - High Performance Polyethylene
# MDPE	PE80 - Medium Density Polyethylen
