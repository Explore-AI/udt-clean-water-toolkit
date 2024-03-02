from .point_asset import PointAsset
from cwa_geod.core.constants import LOGGER_NAME


class Logger(PointAsset):
    class AssetMeta:
        asset_name = LOGGER_NAME
