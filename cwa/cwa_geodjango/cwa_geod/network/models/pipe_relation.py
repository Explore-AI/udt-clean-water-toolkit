from neomodel import StructuredRel, StringProperty, FloatProperty


class PipeRelation(StructuredRel):
    gid = StringProperty(unique_index=True, required=True)
    dmas = StringProperty(required=True)
    weight = FloatProperty(required=True)
