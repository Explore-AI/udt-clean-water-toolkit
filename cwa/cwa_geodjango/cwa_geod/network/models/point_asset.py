from neomodel import StructuredNode, StringProperty, Relationship
from .trunk_main import TrunkMain


class PointAsset(StructuredNode):
    gid = StringProperty(unique_index=True, required=True)
    dmas = StringProperty(required=True)
    trunk_main = Relationship("PointNode", "TRUNKMAIN", model=TrunkMain)
