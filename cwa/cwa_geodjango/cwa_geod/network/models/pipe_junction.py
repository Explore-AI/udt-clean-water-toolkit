from neomodel import ArrayProperty
from .point_node import PointNode
from cwa_geod.core.constants import PIPE_JUNCTION__NAME


class PipeJunction(PointNode):

    class AssetMeta:
        node_type = PIPE_JUNCTION__NAME
