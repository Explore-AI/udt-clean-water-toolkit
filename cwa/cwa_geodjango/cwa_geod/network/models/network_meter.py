from .point_asset import PointAsset
from cwa_geod.core.constants import NETWORK_METER_NAME


class NetworkMeter(PointAsset):
    class AssetMeta:
        asset_name = NETWORK_METER_NAME
