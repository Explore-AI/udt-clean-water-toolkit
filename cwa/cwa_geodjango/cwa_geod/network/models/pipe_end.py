from neomodel import StringProperty
from .point_node import PointNode
from cwa_geod.core.constants import PIPE_ASSETS__NAMES


class PipeEnd(PointNode):
    pipe_type = StringProperty(required=True, index=True, choices=PIPE_ASSETS__NAMES)
    pipe_segment_id = StringProperty(required=True, index=True)

    class AssetMeta:
        asset_name = "pipe_end"
