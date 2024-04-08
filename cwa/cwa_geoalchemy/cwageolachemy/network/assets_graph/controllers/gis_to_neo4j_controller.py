from ...assets_gis.controllers.trunk_mains_controller import TrunkMainsController
from ...assets_gis.controllers.distribution_mains_controller import (
    DistributionMainsController,
)
from cwageolachemy.network.assets_gis.models import *


class GisToNeo4jController:
    def __init__(self) -> None:
        pass

    def create_network(self):
        pass

    def _get_pipe_and_asset_data(self):
        trunk_mains_statement = self.get_trunk_mains_data()
        # distribution_mains_statement = ""

    def get_trunk_mains_data(self):
        tm: TrunkMainsController = TrunkMainsController()
        return tm.get_pipe_point_relation_queryset(
            model=TrunkMain, main_dmas=trunkmain_dmas
        )

    def get_distribution_mains_data(self):
        dm: DistributionMainsController = DistributionMainsController()
        return dm.get_pipe_point_relation_queryset(
            model=DistributionMain, main_dmas=distributionmain_dmas
        )
