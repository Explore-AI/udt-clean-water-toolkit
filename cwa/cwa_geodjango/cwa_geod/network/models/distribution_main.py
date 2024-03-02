from .pipe_relation import PipeRelation
from cwa_geod.core.constants import DISTRIBUTION_MAIN_NAME


class DistributionMain(PipeRelation):
    class AssetMeta:
        asset_name = DISTRIBUTION_MAIN_NAME
