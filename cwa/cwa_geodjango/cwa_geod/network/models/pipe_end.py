from neomodel import StringProperty, install_labels, remove_all_labels
from .point_node import PointNode
from cwa_geod.core.constants import PIPE_ASSETS__NAMES


class PipeEnd(PointNode):
    pipe_type = StringProperty(required=True, index=True, choices=PIPE_ASSETS__NAMES)

    class AssetMeta:
        asset_name = "pipe_end"

    @staticmethod
    def initialise_node_label():
        # setup constraints based on the network.models
        if len(PointNode.nodes.all()) == 0:
            remove_all_labels()
            install_labels(PipeEnd)  # quiet=True
