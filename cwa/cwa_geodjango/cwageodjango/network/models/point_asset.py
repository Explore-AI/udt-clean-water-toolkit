from .point_node import PointNode
from cwageodjango.core.constants import POINT_ASSET__NAME


class PointAsset(PointNode):

    class AssetMeta:
        node_type = POINT_ASSET__NAME
