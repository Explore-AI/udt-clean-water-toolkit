from neomodel import StructuredRel, StringProperty


class HasDma(StructuredRel):
    code = StringProperty(index=True, required=True)
    name = StringProperty(index=True, required=True)
