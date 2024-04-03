from abc import ABC, abstractmethod
from sqlalchemy.dialects.postgresql import array_agg, array
from ..models import TrunkMain, DistributionMain
from typing import Any, List, Optional 


class MainsController(ABC): 
    WITHIN_DISTANCE = 0.5 
    default_properties = [
        "id", 
        "gid"
    ]

    def _generate_dwithin_subquery(self) -> Any:
        pass 

    def _generate_touches_subquery(self) -> Any: 
        pass 
    
    @staticmethod
    def get_asset_json_fields() -> dict: 
        pass 
    
    @staticmethod
    def get_pipe_json_fields() -> dict: 
        pass 
    
    @abstractmethod
    def _generate_mains_subqueries(self) -> Any: 
        pass
    
    def _generate_asset_subqueries(self) -> Any: 
        pass 
    
    def get_pipe_point_relation_queryset(self) -> Any:
        pass 
    
    def get_geometry_queryset(self) -> Any:
        pass

    def mains_to_geojson(self, properties=None) -> Any: 
        pass 
    
    def mains_to_geojson2(self, properties=None) -> Any:
        pass 
    
    def mains_to_geodataframe(self, properties=None) -> Any:
        pass
    
    
