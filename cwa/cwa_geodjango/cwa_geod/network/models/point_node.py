from neomodel import (
    StructuredNode,
    RelationshipTo,
    IntegerProperty,
    JSONProperty,
    install_labels,
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


# install_labels(PointNode)
