from .point_asset import PointAsset
from cwa_geod.core.constants import NETWORK_OPT_VALVE_NAME


class NetworkOptValve(PointAsset):
    class AssetMeta:
        asset_name = NETWORK_OPT_VALVE_NAME
