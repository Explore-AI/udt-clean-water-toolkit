from .point_asset import PointAsset
from cwa_geod.core.constants import CHAMBER__NAME


class Chamber(PointAsset):
    class AssetMeta:
        asset_name = CHAMBER__NAME
