from neomodel import ArrayProperty
from .point_node import PointNode
from cwa_geod.core.constants import PIPE_JUNCTION__NAME


class PipeJunction(PointNode):
    gids = ArrayProperty(required=True, index=True)
    # pipe_types = ArrayProperty(required=True, index=True)

    class AssetMeta:
        node_type = PIPE_JUNCTION__NAME
