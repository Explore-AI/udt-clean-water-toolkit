from .point_asset import PointAsset
from cwa_geod.core.constants import HYDRANT__NAME


class Hydrant(PointAsset):
    class AssetMeta:
        asset_name = HYDRANT__NAME
