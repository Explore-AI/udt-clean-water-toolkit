from collections import OrderedDict
from cwageodjango.assets.models import *

POINT_ASSET_MODELS = OrderedDict(
    [
        ("borehole", Borehole),
        ("bulk_meter", BulkMeter),
        ("chamber", Chamber),
        ("connection_meter", ConnectionMeter),
        ("consumption_meter", ConsumptionMeter),
        ("hydrant", Hydrant),
        ("isolation_valve", IsolationValve),
        ("logger", Logger),
        ("network_meter", NetworkMeter),
        ("nonreturn_valve", NonReturnValve),
        ("operational_site", OperationalSite),
        ("potable_water_storage", PotableWaterStorage),
        ("pressure_control_valve", PressureControlValve),
        ("pressure_fitting", PressureFitting),
        ("regulator", Regulator),
        ("revenue_meter", RevenueMeter),
        ("water_facility_connection", WaterFacilityConnection),
        ("water_pipe_connection", WaterPipeConnection),
        ("water_pumping_facility", WaterPumpingFacility),
        ("water_treatment_work", WaterTreatmentWork),
    ]
)

PIPE_MAIN_MODEL = PipeMain
