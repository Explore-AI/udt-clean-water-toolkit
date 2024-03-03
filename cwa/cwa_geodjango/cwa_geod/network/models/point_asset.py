from neomodel import StringProperty
from .point_node import PointNode


class PointAsset(PointNode):
    class AssetMeta:
        asset_name = "point_asset"
