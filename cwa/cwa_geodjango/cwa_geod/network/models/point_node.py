from neomodel import (
    StructuredNode,
    RelationshipTo,
    FloatProperty,
    StringProperty,
    JSONProperty,
    ZeroOrOne,
)
from neomodel.contrib.spatial_properties import PointProperty
from .trunk_main import TrunkMain
from .distribution_main import DistributionMain
from cwa_geod.core.constants import UTILITIES


class PointNode(StructuredNode):
    dmas = JSONProperty(required=True)
    # location = PointProperty(crs="wgs-84", require=True)
    x_coord = FloatProperty(required=True)
    y_coord = FloatProperty(required=True)
    node_id = StringProperty(unique_index=True, unique=True, required=True)
    utility = StringProperty(required=True, index=True, choices=UTILITIES)
    trunk_main = RelationshipTo(
        "PointNode", "trunk_main", model=TrunkMain, cardinality=ZeroOrOne
    )
    distribution_main = RelationshipTo(
        "PointNode", "distribution_main", model=DistributionMain, cardinality=ZeroOrOne
    )
