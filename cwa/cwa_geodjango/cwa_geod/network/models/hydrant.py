from neomodel import StructuredNode, StringProperty


class Hydrant(StructuredNode):
    gid = StringProperty(unique_index=True, required=True)
