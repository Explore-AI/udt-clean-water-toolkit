from neomodel import (
    StructuredNode,
    Relationship,
    ArrayProperty,
    StringProperty,
    BooleanProperty,
)
from neomodel.contrib.spatial_properties import PointProperty
from .pipe_main import PipeMain
from .has_dma import HasDma
from cwageodjango.core.constants import UTILITIES


class NetworkNode(StructuredNode):
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
    node_key = StringProperty(unique=True, index=True, required=True)
    subtype = StringProperty(index=True)
    acoustic_logger = BooleanProperty(index=True)
    node_types = ArrayProperty(required=True, index=True)
    asset_names = ArrayProperty(required=True, index=True)
    asset_gids = ArrayProperty(required=True, index=True)
    location = PointProperty(crs="wgs-84", require=True)
    pipe_main = Relationship("PipeMain", "pipe_main", model=PipeMain)
    has_dma = Relationship("HAS_DMA", "has_dma", model=HasDma)
