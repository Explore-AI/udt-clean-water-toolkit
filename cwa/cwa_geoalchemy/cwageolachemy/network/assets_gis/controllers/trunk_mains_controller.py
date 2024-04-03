from .mains_controller import MainsController
from ..models import TrunkMain
from typing import Any, List, Optional 


class TrunkMainsController(MainsController): 
    model = TrunkMain
    
    def _generate_mains_subqueries(self):
        pass 
    
    def trunk_mains_to_geojson(self, properties=None): 
        pass 
    
    def trunk_mains_to_geojson2(self, properties=None):
        pass 
    
    def trunk_mains_to_geodataframe(self, properties=None):
        pass 