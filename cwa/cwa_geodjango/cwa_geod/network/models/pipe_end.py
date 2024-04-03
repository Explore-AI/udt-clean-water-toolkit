from neomodel import IntegerProperty
from .point_node import PointNode
from cwa_geod.core.constants import PIPE_END__NAME


class PipeEnd(PointNode):
    gid = IntegerProperty(index=True, required=True)

    class AssetMeta:
        node_type = PIPE_END__NAME
