from collections import OrderedDict
from cwageodjango.assets.models import Logger, Hydrant, NetworkMeter, PipeMain

POINT_ASSET_MODELS = OrderedDict(
    [("logger", Logger), ("hydrant", Hydrant), ("network_meter", NetworkMeter)]
)

PIPE_MAIN_MODEL = PipeMain
