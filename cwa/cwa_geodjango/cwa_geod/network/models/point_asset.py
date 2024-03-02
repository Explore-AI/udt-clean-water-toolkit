from neomodel import StringProperty
from .point_node import PointNode


class PointAsset(PointNode):
    dmas = StringProperty(required=True)
