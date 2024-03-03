from neomodel import StringProperty
from .point_node import PointNode
from cwa_geod.core.constants import PIPE_ASSETS__NAMES


class PipeEnd(PointNode):
    pipe_type = StringProperty(required=True, choices=PIPE_ASSETS__NAMES)

    class AssetMeta:
        asset_name = "pipe_end"
