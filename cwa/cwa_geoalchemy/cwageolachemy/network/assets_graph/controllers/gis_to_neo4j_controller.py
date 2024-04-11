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
        print(f"Fully implemented sql query")
        print(pipes_query)
        print('-'*100)
        
        # with Session(engine) as session:
        #     query_results = session.execute(pipes_query)
        #     print(query_results)

        #     for result in query_results:
        #         print(result)

    def _get_pipe_and_asset_data(self):
        trunk_mains_statement = self.get_trunk_mains_data()
        distribution_mains_statement = self.get_distribution_mains_data()
        # print(f"Fully implemented trunk mains sql query")
        # print(trunk_mains_statement)
        # print('-'*100)
        # print(f"Fully implemented distribution mains sql query")
        # print(distribution_mains_statement)
        # print('-'*100)  
        unioned_query = trunk_mains_statement.union_all(distribution_mains_statement)
        print(f"Unioned query")
        print(unioned_query)
        print('-'*100)
        
        with Session(engine) as session: 
            # run the tm statmeent 
            tm_result = session.execute(trunk_mains_statement)
            for result in tm_result: 
                print(result)
            
            # print('-'*100)
            # dm_result = session.execute(distribution_mains_statement)
            # for result in dm_result:
            #     print(result)
            # print("-"*100)
            
            # unioned_result = session.execute(unioned_query)
            # for result in unioned_result:
            #     print(result)
            print("-"*100)
            
        # unioned_query = trunk_mains_statement.union_all(distribution_mains_statement)

        # return unioned_query

    def get_trunk_mains_data(self):
        tm: TrunkMainsController = TrunkMainsController()
        # test the subqueries
        return tm.get_pipe_point_relation_queryset(
            model=TrunkMain, main_dmas=trunkmain_dmas
        )

    def get_distribution_mains_data(self):
        dm: DistributionMainsController = DistributionMainsController()
        return dm.get_pipe_point_relation_queryset(
            model=DistributionMain, main_dmas=distributionmain_dmas
        )
