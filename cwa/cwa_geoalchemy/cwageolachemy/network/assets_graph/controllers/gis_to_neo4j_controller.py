from cwageolachemy.network.assets_gis.controllers.trunk_mains_controller import (
    TrunkMainsController,
)
from ...assets_gis.controllers.distribution_mains_controller import (
    DistributionMainsController,
)
from cwageolachemy.network.assets_gis.models import *
from cwageolachemy.network.assets_utilities.models import *
from sqlalchemy.orm import Session
from sqlalchemy import select, func, Integer
from sqlalchemy.dialects.postgresql import array_agg, array, ARRAY, JSONB
from cwageolachemy.config.db_config import engine
from sqlalchemy.orm import aliased, Query, joinedload


class GisToNeo4jController:
    def __init__(self) -> None:
        pass

    def create_network(self):
        pipes_query = self._get_pipe_and_asset_data()
        
        with Session(engine) as session:
            count = 0 
            for pipe_data in session.execute(pipes_query).fetchall():
                if count == 10: 
                    break
                else: 
                    print(pipe_data)
                    print('_'*100)
                    count += 1

    def _get_pipe_and_asset_data(self):
        trunk_mains_statement = self.get_trunk_mains_data()
        distribution_mains_statement = self.get_distribution_mains_data()

        unioned_query = trunk_mains_statement.union_all(distribution_mains_statement)
        return unioned_query

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
