from abc import ABC, abstractmethod
from sqlalchemy.dialects.postgresql import array_agg, array
from sqlalchemy.sql import Select
from sqlalchemy.orm import aliased, Query
from geoalchemy2.functions import (
    ST_AsGeoJSON,
    ST_AsEWKT,
    ST_StartPoint,
    ST_EndPoint,
    ST_Touches,
)
from ..models import TrunkMain, DistributionMain
from cwageolachemy.network.assets_utilities.models import Utility, DMA
from typing import Any, List, Optional


class MainsController(ABC):
    WITHIN_DISTANCE = 0.5
    default_properties = ["id", "gid"]

    def _generate_dwithin_subquery(
        self, stmt_set, json_fields, geometry_field="geometry", inner_stmts={}
    ) -> Any:

        pass

    @staticmethod
    def generate_touches_subquery(
        qs: Query, json_fields: dict, geometry_field: str = "geometry"
    ) -> Any:

        dma_alias = aliased(DMA)
        model = qs.column_descriptions[0]["entity"]
        # create the touches condition 
        touches_condition = ST_Touches(getattr(model, geometry_field))

        subquery = qs.filter(touches_condition)
        
        # :TODO instead of for loop implement it subsequentially
        # for k, v in json_fields.items(): 
        #     if isinstance(v, array): 
        #         subquery = subquery.add_columns(array_agg(dma_alias.id).label("dma_ids"))
        #     elif k == "wkt": 
        #         subquery = subquery.add_columns(ST_AsEWKT(getattr(model, geometry_field)).label(k))
        #     else: 
        #         subquery = subquery.add_columns(getattr(dma_alias, k).label(k))
        
        return subquery
        

    @staticmethod
    def get_asset_json_fields(geometry_field="geometry") -> dict:
        return {
            "id": "id",
            "gid": "gid",
            "geometry": geometry_field,
            "wkt": ST_AsEWKT(geometry_field),
            "dma_ids": array_agg(array("dmas")),
            "dma_names": array_agg(array("dma__name")),
            "dma_codes": array_agg(array("dma__code")),
            "utilities": array_agg(array("dmas__utility__name")),
        }

    @staticmethod
    def get_pipe_json_fields() -> dict:

        return {
            "id": "id",
            "gid": "gid",
            "geometry": "geometry",
            "wkt": ST_AsEWKT("geometry"),
            "start_point": ST_StartPoint("geometry"),
            "end_point": ST_EndPoint("geometry"),
            "dma_ids": array_agg(array("dmas")),
            "dma_names": array_agg(array("dma__name")),
            "dma_codes": array_agg(array("dma__code")),
            "utilities": array_agg(array("dmas__utility__name")),
        }

    @abstractmethod
    def _generate_mains_subqueries(self) -> Any:
        pass

    def _generate_asset_subqueries(self) -> Any:
        pass

    def get_pipe_point_relation_queryset(self) -> Any:
        mains_intersection_stmt = self._generate_mains_subqueries()
        asset_stmt = self._generate_asset_subqueries()

    def get_geometry_queryset(self) -> Any:
        pass

    def mains_to_geojson(self, properties=None) -> Any:
        pass

    def mains_to_geojson2(self, properties=None) -> Any:
        pass

    def mains_to_geodataframe(self, properties=None) -> Any:
        pass
