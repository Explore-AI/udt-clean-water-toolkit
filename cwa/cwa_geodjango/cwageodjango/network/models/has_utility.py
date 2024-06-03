from neomodel import StructuredRel, StringProperty


class HasUtility(StructuredRel):
    name = StringProperty(index=True, required=True)
