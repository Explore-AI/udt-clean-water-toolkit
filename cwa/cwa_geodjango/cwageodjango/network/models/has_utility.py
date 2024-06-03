from neomodel import StructuredRel, StringProperty


class HasUtility(StructuredRel):
    name = StringProperty(unique=True, index=True, required=True)
