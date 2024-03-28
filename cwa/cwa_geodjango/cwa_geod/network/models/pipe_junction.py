from neomodel import ArrayProperty, StringProperty
from .point_node import PointNode


class PipeJunction(PointNode):
    gids = ArrayProperty(required=True, index=True)
    pipe_types = ArrayProperty(required=True, index=True)
    junction_id = StringProperty(unique_index=True, unique=True, required=True)

    class AssetMeta:
        asset_name = "pipe_junction"
