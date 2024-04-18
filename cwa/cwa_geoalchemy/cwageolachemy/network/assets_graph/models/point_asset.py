from neomodel import IntegerProperty, StringProperty
from .point_node import PointNode

POINT_ASSET__NAME = "point_asset"

class PointAsset(PointNode):
    gid = IntegerProperty(unique_index=True, unique=True, required=True)

    class AssetMeta:
        node_type = POINT_ASSET__NAME