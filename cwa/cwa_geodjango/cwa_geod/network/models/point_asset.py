from neomodel import IntegerProperty, StringProperty
from .point_node import PointNode
from cwa_geod.core.constants import POINT_ASSET__NAME


class PointAsset(PointNode):
    gid = IntegerProperty(unique_index=True, unique=True, required=True)

    class AssetMeta:
        node_type = POINT_ASSET__NAME
