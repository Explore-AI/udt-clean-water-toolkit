from neomodel import ArrayProperty
from .point_node import PointNode 

PIPE_JUNCTION__NAME = "pipe_junction"

class PipeJunction(): 
    pipe_gids = ArrayProperty(required=True, index=True)
    
    class AssetMeta: 
        node_type = PIPE_JUNCTION__NAME
    