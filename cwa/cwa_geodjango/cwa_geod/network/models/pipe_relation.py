from neomodel import StructuredRel, IntegerProperty, JSONProperty, StringProperty


class PipeRelation(StructuredRel):
    # relation_id = StringProperty(unique=True, index=True, required=True)
    gid = IntegerProperty(index=True, required=True)
    utility = StringProperty(index=True, required=True)
    # length = IntegerProperty(required=True)
    dmas = JSONProperty(required=True)
