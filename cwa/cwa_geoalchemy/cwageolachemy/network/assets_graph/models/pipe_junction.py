from neomodel import ArrayProperty
from . import NetworkNode

PIPE_JUNCTION__NAME = "pipe_junction"

class PipeJunction(NetworkNode):
    pipe_gids = ArrayProperty(required=True, index=True)
    
    class AssetMeta: 
        node_type = PIPE_JUNCTION__NAME
