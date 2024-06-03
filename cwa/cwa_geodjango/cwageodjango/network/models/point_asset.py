from . import NetworkNode
from cwageodjango.core.constants import POINT_ASSET__NAME


class PointAsset(NetworkNode):

    class AssetMeta:
        node_type = POINT_ASSET__NAME
