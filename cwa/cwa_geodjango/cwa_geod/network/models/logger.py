from .point_asset import PointAsset
from cwa_geod.core.constants import LOGGER__NAME


class Logger(PointAsset):
    class AssetMeta:
        asset_name = LOGGER__NAME
