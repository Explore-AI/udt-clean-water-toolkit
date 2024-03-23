from neomodel import (
    StructuredNode,
    RelationshipTo,
    IntegerProperty,
    StringProperty,
    JSONProperty,
)
from neomodel.contrib.spatial_properties import PointProperty
from .trunk_main import TrunkMain
from .distribution_main import DistributionMain
from cwa_geod.core.constants import UTILITIES


class PointNode(StructuredNode):
    gid = IntegerProperty(unique_index=True, unique=True, required=True)
    dmas = JSONProperty(required=True)
    location = PointProperty(crs="wgs-84")
    utility = StringProperty(required=True, index=True, choices=UTILITIES)
    trunk_main = RelationshipTo("PointNode", "TRUNKMAIN", model=TrunkMain)
    distribution_main = RelationshipTo(
        "PointNode", "DISTRIBUTIONMAIN", model=DistributionMain
    )
