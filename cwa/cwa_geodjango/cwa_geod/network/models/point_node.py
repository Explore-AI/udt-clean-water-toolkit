from neomodel import StructuredNode, StringProperty, Relationship
from .trunk_main import TrunkMain


class PointNode(StructuredNode):
    gid = StringProperty(unique_index=True, required=True)
    dmas = StringProperty(unique_index=True, required=True)
    trunk_mains = Relationship("PointNode", "TRUNKMAIN", model=TrunkMain)
