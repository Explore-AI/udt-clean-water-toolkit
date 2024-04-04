from abc import ABC, abstractmethod
from sqlalchemy.dialects.postgresql import array_agg, array
from sqlalchemy.sql import Select, cast
from sqlalchemy import func, select
from sqlalchemy.orm import aliased, Query
from sqlalchemy.sql.expression import literal_column
from geoalchemy2 import functions as geo_funcs
from ..models import TrunkMain, DistributionMain, trunkmain_dmas
from cwageolachemy.network.assets_utilities.models import Utility, DMA
from typing import Any, List, Optional, Union


class MainsController(ABC):
    WITHIN_DISTANCE = 0.5
    default_properties = ["id", "gid"]

    def _generate_dwithin_subquery(
        self, stmt_set, json_fields, geometry_field="geometry", inner_stmts={}
    ) -> Any:

        pass

    @staticmethod
    def generate_touches_subquery(
        stmt: Select,
        json_fields: dict,
        model: Union[TrunkMain, DistributionMain],
        geometry_field: str = "geometry",
    ) -> Any:
        # :TODO Make this a Dynamic function

        trunkmain_dmas_alias = aliased(trunkmain_dmas)
        dma_alias = aliased(DMA)
        utility_alias = aliased(Utility)
        print(f"Model from entity: {model}")

        # create the touches condition
        json_object_subquery = select(
            func.json_build_object(
                "id",
                model.id,
                "gid",
                model.gid,
                "geometry",
                model.geometry,
                "wkt",
                geo_funcs.ST_AsText(getattr(model, geometry_field)),
                "dma_ids",
                array_agg(dma_alias.id),
                "dma_names",
                array_agg(dma_alias.name),
                "dma_codes",
                array_agg(dma_alias.code),
                "utilities",
                array_agg(utility_alias.name),
                "asset_name",
                literal_column(model.AssetMeta.asset_name),
            ).label("json"),
        )
        sub_query = (
            json_object_subquery.join(
                trunkmain_dmas_alias, model.id == trunkmain_dmas_alias.c.trunkmain_id
            )
            .join(dma_alias, trunkmain_dmas.c.dma_id == dma_alias.id)
            .join(utility_alias, dma_alias.utility_id == utility_alias.id)
            .where(geo_funcs.ST_Touches(model.geometry, (model.geometry)))
            .group_by(
                model.id,
                geo_funcs.ST_AsText(model.geometry),
                geo_funcs.ST_StartPoint(model.geometry),
                geo_funcs.ST_EndPoint(model.geometry),
            )
        )

        return sub_query

    @staticmethod
    def get_asset_json_fields(geometry_field="geometry") -> dict:
        return {
            "id": "id",
            "gid": "gid",
            "geometry": geometry_field,
            "wkt": geo_funcs.ST_AsText(geometry_field),
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
            "wkt": geo_funcs.ST_AsText("geometry"),
            "start_point": geo_funcs.ST_StartPoint("geometry"),
            "end_point": geo_funcs.ST_EndPoint("geometry"),
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
