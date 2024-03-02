from .pipe_relation import PipeRelation
from cwa_geod.core.constants import TRUNK_MAIN_NAME


class TrunkMain(PipeRelation):
    class AssetMeta:
        asset_name = TRUNK_MAIN_NAME
