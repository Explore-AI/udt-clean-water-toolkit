from neomodel import (
    StructuredNode,
    Relationship,
    FloatProperty,
    StringProperty,
    JSONProperty,
    ZeroOrOne,
)
from neomodel.contrib.spatial_properties import PointProperty
from .pipe_relation import PipeRelation
from cwa_geod.core.constants import UTILITIES


class PointNode(StructuredNode):
    dmas = JSONProperty(required=True)
    # location = PointProperty(crs="wgs-84", require=True)
    x_coord = FloatProperty(required=True)
    y_coord = FloatProperty(required=True)
    node_id = StringProperty(unique_index=True, unique=True, required=True)
    utility = StringProperty(required=True, index=True, choices=UTILITIES)
    pipe_relation = Relationship("PipeRelation", "pipe_relation", model=PipeRelation)
