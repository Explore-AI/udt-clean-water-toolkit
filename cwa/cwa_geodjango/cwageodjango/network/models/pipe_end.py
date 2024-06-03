from .network_node import NetworkNode
from cwageodjango.core.constants import PIPE_END__NAME


class PipeEnd(NetworkNode):
    class AssetMeta:
        node_type = PIPE_END__NAME
