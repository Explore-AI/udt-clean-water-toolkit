from neomodel import StructuredRel, IntegerProperty, FloatProperty, JSONProperty


class PipeRelation(StructuredRel):
    gid = IntegerProperty(unique_index=True, unique=True, required=True)
    dmas = JSONProperty(required=True)
    weight = FloatProperty(required=True)
