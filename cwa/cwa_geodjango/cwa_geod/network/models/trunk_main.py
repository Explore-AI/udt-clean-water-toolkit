from neomodel import StructuredRel, StringProperty


class TrunkMain(StructuredRel):
    gid = StringProperty(unique_index=True, required=True)
    dmas = StringProperty(unique_index=True, required=True)
