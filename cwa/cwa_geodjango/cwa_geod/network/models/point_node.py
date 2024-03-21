from neomodel import (
    StructuredNode,
    RelationshipTo,
    IntegerProperty,
    JSONProperty,
    install_labels,
    remove_all_labels,
)
from neomodel.contrib.spatial_properties import PointProperty
from .trunk_main import TrunkMain
from .distribution_main import DistributionMain


class PointNode(StructuredNode):
    gid = IntegerProperty(unique_index=True, unique=True, required=True)
    dmas = JSONProperty(required=True)
    location = PointProperty(crs="wgs-84")
    trunk_main = RelationshipTo("PointNode", "TRUNKMAIN", model=TrunkMain)
    distribution_main = RelationshipTo(
        "PointNode", "DISTRIBUTIONMAIN", model=DistributionMain
    )

    def initialise_node_label(self):
        # setup constraints based on the network.models
        if len(PointNode.nodes.all()) == 0:
            remove_all_labels()
            install_labels(PointNode)  # quiet=True
