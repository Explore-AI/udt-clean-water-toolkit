from neomodel import IntegerProperty
from .network_asset import NetworkAsset
from cwageodjango.core.constants import POINT_ASSET__NAME


class PointAsset(NetworkAsset):
    __optional_labels__ = [
        "NetworkOptValve",
        "Hydrant",
        "NetworkMeter",
        "OperationalSite",
        "Logger",
        "Chamber",
        "PressureFitting",
        "PressureControlValve",
        "ConnectionMeter",
        "ConsumptionMeter",
    ]

    gid = IntegerProperty(required=True, index=True)

    class AssetMeta:
        node_type = POINT_ASSET__NAME
