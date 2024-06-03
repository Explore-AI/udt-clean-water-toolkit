from neomodel import (
    StructuredNode,
    Relationship,
    ArrayProperty,
    StringProperty,
    JSONProperty,
)
# from neomodel.contrib.spatial_properties import PointProperty
from .pipe_relation import PipeRelation


UTILITIES = [
    ("thames_water", "Thames Water"),
    ("severn_trent_water", "Severn Trent Water"),
]

class NetworkNode(StructuredNode):
    __abstract__ = True
    dmas = JSONProperty(required=True)
    coords_27700 = ArrayProperty(required=True)
    node_id = StringProperty(unique_index=True, unique=True, required=True)
    utility = StringProperty(required=True, index=True, choices=UTILITIES)
    pipe_relation = Relationship("PipeRelation", "pipe_relation", model=PipeRelation)
