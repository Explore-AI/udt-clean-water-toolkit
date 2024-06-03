from neomodel import (
    StructuredNode,
    StringProperty,
)
from neomodel.contrib.spatial_properties import PointProperty
from .pipe_main import PipeMain
from .has_dma import HasDma
from .has_utility import HasUtility
from cwageodjango.core.constants import UTILITIES


class Dma(StructuredNode):
    code = StringProperty(required=True, index=True)
    name = StringProperty(required=True, index=True)
