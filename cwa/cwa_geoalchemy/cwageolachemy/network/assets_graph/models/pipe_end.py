from neomodel import IntegerProperty
from .point_node import PointNode

PIPE_END__NAME = "pipe_end"

class PipeEnd(PointNode):
    gid = IntegerProperty(index=True, required=True)

    class AssetMeta:
        node_type = PIPE_END__NAME
