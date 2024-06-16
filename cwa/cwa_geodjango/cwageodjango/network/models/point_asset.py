from neomodel import IntegerProperty
from .network_node import NetworkNode
from cwageodjango.core.constants import POINT_ASSET__NAME


class PointAsset(NetworkNode):
    __optional_labels__ = [
        "NetworkOptValve",
        "Hydrant",
        "NetworkMeter",
        "OperationalSite",
        "Logger",
        "Chamber",
        "PressureFitting",
        "PressureControlValve",
    ]

    gid = IntegerProperty(required=True, index=True)

    class AssetMeta:
        node_type = POINT_ASSET__NAME
