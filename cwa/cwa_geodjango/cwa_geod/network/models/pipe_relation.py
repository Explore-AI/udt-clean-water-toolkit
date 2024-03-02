from neomodel import StructuredRel, StringProperty, FloatProperty, JSONProperty


class PipeRelation(StructuredRel):
    gid = StringProperty(unique_index=True, required=True)
    dmas = JSONProperty(required=True)
    weight = FloatProperty(required=True)
