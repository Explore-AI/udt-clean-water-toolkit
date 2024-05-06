from .point_node import PointNode
from cwageodjango.core.constants import PIPE_END__NAME


class PipeEnd(PointNode):
    class AssetMeta:
        node_type = PIPE_END__NAME
