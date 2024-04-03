from .mains_controller import MainsController
from ..models import TrunkMain, DistributionMain
from typing import Any, List, Optional 
from cwageolachemy.config.db_config import engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import array as ARRAY



class TrunkMainsController(MainsController): 
    model = TrunkMain
    
    def _generate_mains_subqueries(self):
        print("Generate the mains subqueries")
        with Session(engine) as session:
            # create query distribution and trunk query sets 
            tm_query = session.query(self.model)
            dm_query = session.query(DistributionMain)
            
            json_fields = self.get_asset_json_fields()
            subquery_tm_junctions = self.generate_touches_subquery(tm_query, json_fields)
            print(subquery_tm_junctions)
            
            
    def trunk_mains_to_geojson(self, properties=None): 
        pass 
    
    def trunk_mains_to_geojson2(self, properties=None):
        pass 
    
    def trunk_mains_to_geodataframe(self, properties=None):
        pass 