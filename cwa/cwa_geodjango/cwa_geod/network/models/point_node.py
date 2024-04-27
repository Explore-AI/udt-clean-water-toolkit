from neomodel import (
    StructuredNode,
    Relationship,
    ArrayProperty,
    StringProperty,
    JSONProperty,
)
from neomodel.contrib.spatial_properties import PointProperty
from .pipe_main import PipeMain
from cwa_geod.core.constants import UTILITIES


class PointNode(StructuredNode):
    __abstract__ = True
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

    utility = StringProperty(required=True, index=True, choices=UTILITIES)
    coords_27700 = ArrayProperty(required=True)
    node_key = StringProperty(unique_index=True, unique=True, required=True)
    dmas = JSONProperty(required=True)
    node_types = ArrayProperty(required=True, index=True)
    asset_names = ArrayProperty(required=True, index=True)
    asset_gids = ArrayProperty(required=True, index=True)
    # location = PointProperty(crs="wgs-84", require=True)
    pipe_main = Relationship("PipeMain", "pipe_main", model=PipeMain)
