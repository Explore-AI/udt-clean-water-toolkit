from neomodel import StructuredRel, IntegerProperty, JSONProperty, StringProperty


class PipeRelation(StructuredRel):
    gid = IntegerProperty(unique_index=True, unique=True, required=True)
    utility = StringProperty(index=True, unique=True, required=True)
    length = IntegerProperty(required=True)
    dmas = JSONProperty(required=True)
