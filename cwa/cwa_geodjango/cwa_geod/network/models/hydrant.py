from .point_asset import PointAsset
from cwa_geod.core.constants import HYDRANT_NAME


class Hydrant(PointAsset):
    class AssetMeta:
        asset_name = HYDRANT_NAME
