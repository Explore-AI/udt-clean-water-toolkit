from .point_asset import PointAsset
from cwa_geod.core.constants import CHAMBER_NAME


class Chamber(PointAsset):
    class AssetMeta:
        asset_name = CHAMBER_NAME
