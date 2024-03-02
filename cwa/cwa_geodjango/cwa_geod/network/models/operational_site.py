from .point_asset import PointAsset
from cwa_geod.core.constants import OPERATIONAL_SITE_NAME


class OperationalSite(PointAsset):
    class AssetMeta:
        asset_name = OPERATIONAL_SITE_NAME
