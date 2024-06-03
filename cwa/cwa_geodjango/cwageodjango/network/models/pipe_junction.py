from . import NetworkNode
from cwageodjango.core.constants import PIPE_JUNCTION__NAME


class PipeJunction(NetworkNode):

    class AssetMeta:
        node_type = PIPE_JUNCTION__NAME
