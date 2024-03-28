from neomodel import ArrayProperty
from .point_node import PointNode


class PipeJunction(PointNode):
    gid = None
    gids = ArrayProperty(required=True, index=True)

    class AssetMeta:
        asset_name = "pipe_junction"
