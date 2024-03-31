from neomodel import StructuredRel, IntegerProperty, JSONProperty, StringProperty


class PipeRelation(StructuredRel):
    gid = IntegerProperty(index=True, required=True)
    utility = StringProperty(index=True, required=True)
    # length = IntegerProperty(required=True)
    dmas = JSONProperty(required=True)
