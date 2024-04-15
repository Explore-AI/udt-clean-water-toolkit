from neomodel import StructuredRel, IntegerProperty, StringProperty


class PipeRelation(StructuredRel):
    from_node_id = StringProperty(index=True, required=True)
    to_node_id = StringProperty(index=True, required=True)
    gid = IntegerProperty(index=True, required=True)
    utility = StringProperty(index=True, required=True)
    # length = IntegerProperty(required=True)
