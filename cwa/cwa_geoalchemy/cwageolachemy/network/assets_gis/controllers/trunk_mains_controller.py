from .mains_controller import MainsController
from ..models import TrunkMain
from typing import Any, List, Optional 
from cwageolachemy.config.db_config import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select



class TrunkMainsController(MainsController): 
    model = TrunkMain
    
    def _generate_mains_subqueries(self):
        with Session(create_engine()) as session:
            statement = select(TrunkMain).where(TrunkMain.id == 123456)
            result = session.scalars(statement).one()
            print(f"Our result: {result}")
    
    def trunk_mains_to_geojson(self, properties=None): 
        pass 
    
    def trunk_mains_to_geojson2(self, properties=None):
        pass 
    
    def trunk_mains_to_geodataframe(self, properties=None):
        pass 