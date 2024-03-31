from neomodel import StringProperty, IntegerProperty
from .point_node import PointNode
from cwa_geod.core.constants import PIPE_END__NAME, PIPE_ASSETS__CHOICES


class PipeEnd(PointNode):
    gid = IntegerProperty(unique_index=True, unique=True, required=True)
    pipe_type = StringProperty(required=True, index=True, choices=PIPE_ASSETS__CHOICES)

    class AssetMeta:
        node_type = PIPE_END__NAME
