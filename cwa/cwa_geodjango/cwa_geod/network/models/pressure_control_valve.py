from .point_asset import PointAsset
from cwa_geod.core.constants import PRESSURE_CONTROL_VALVE_NAME


class PressureControlValve(PointAsset):
    class AssetMeta:
        asset_name = PRESSURE_CONTROL_VALVE_NAME
