from neomodel import StructuredRel, StringProperty


class HasDma(StructuredRel):
    code = StringProperty(unique=True, index=True, required=True)
    name = StringProperty(unique=True, index=True, required=True)
