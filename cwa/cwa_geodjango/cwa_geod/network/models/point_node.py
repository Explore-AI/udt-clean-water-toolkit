from neomodel import (
    StructuredNode,
    Relationship,
    ArrayProperty,
    StringProperty,
    JSONProperty,
)
from neomodel.contrib.spatial_properties import PointProperty
from .pipe_relation import PipeRelation
from cwa_geod.core.constants import UTILITIES


class PointNode(StructuredNode):
    __abstract__ = True
    dmas = JSONProperty(required=True)
    # location = PointProperty(crs="wgs-84", require=True)
    gids = ArrayProperty(required=True, index=True)
    asset_names = ArrayProperty(required=True, index=True)
    coords_27700 = ArrayProperty(required=True)
    node_key = StringProperty(unique_index=True, unique=True, required=True)
    utility = StringProperty(required=True, index=True, choices=UTILITIES)
    pipe_relation = Relationship("PipeRelation", "pipe_relation", model=PipeRelation)
