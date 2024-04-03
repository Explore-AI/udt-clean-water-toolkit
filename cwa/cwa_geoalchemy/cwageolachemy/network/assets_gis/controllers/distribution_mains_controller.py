from .mains_controller import MainsController
from ..models import TrunkMain, DistributionMain
from typing import Any, List, Optional 


class DistributionMainsController(MainsController): 
    model = DistributionMain
    
    def _generate_mains_subqueries(self):
        pass 
    
    def distribution_mains_to_geojson(self, properties=None): 
        pass 
    
    def distribution_mains_to_geojson2(self, properties=None):
        pass 
    
    def distribution_mains_to_geodataframe(self, properties=None):
        pass 
    