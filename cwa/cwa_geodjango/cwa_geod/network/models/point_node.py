from neomodel import (
    StructuredNode,
    Relationship,
    StringProperty,
    JSONProperty,
)
from neomodel.contrib.spatial_properties import PointProperty
from .trunk_main import TrunkMain
from .distribution_main import DistributionMain


class PointNode(StructuredNode):
    gid = StringProperty(unique_index=True, required=True)
    dmas = JSONProperty(required=True)
    coords = PointProperty(crs="wgs-84")
    trunk_main = Relationship("PointNode", "TRUNKMAIN", model=TrunkMain)
    distribution_main = Relationship(
        "PointNode", "DISTRIBUTIONMAIN", model=DistributionMain
    )
