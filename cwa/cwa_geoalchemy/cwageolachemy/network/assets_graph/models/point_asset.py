from neomodel import IntegerProperty
from . import NetworkNode

POINT_ASSET__NAME = "point_asset"

class PointAsset(NetworkNode):
    gid = IntegerProperty(unique_index=True, unique=True, required=True)

    class AssetMeta:
        node_type = POINT_ASSET__NAME
