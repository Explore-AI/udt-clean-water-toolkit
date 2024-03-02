from .point_asset import PointAsset
from cwa_geod.core.constants import PRESSURE_FITTING_NAME


class PressureFitting(PointAsset):
    class AssetMeta:
        asset_name = PRESSURE_FITTING_NAME
