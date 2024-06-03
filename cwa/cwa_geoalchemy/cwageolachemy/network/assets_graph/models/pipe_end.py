from neomodel import IntegerProperty
from .network_node import NetworkNode

PIPE_END__NAME = "pipe_end"

class PipeEnd(NetworkNode):
    gid = IntegerProperty(index=True, required=True)

    class AssetMeta:
        node_type = PIPE_END__NAME
