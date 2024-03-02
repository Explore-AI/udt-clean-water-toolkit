from neomodel import StructuredNode, Relationship, StringProperty
from .trunk_main import TrunkMain
from .distribution_main import DistributionMain


class PointNode(StructuredNode):
    gid = StringProperty(unique_index=True, required=True)
    trunk_main = Relationship("PointNode", "TRUNKMAIN", model=TrunkMain)
    distribution_main = Relationship(
        "PointNode", "DISTRIBUTIONMAIN", model=DistributionMain
    )
