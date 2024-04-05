from abc import ABC, abstractmethod
from sqlalchemy.dialects.postgresql import array_agg, array
from sqlalchemy.sql import Select, cast
from sqlalchemy import func, select, String, Text, Table, literal_column
from sqlalchemy.orm import aliased, Query
from sqlalchemy.sql.expression import literal_column
from geoalchemy2 import functions as geo_funcs
from ..models import TrunkMain, DistributionMain, trunkmain_dmas, distributionmain_dmas
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
        model: Optional[Union[TrunkMain, DistributionMain]],
        associate_dmas_model: Optional[Table],
        geometry_field: str = "geometry",
    ) -> Any:
        # :TODO Make this a Dynamic function

        main_dmas_alias = aliased(associate_dmas_model)
        dma_alias = aliased(DMA)
        utility_alias = aliased(Utility)
        sub_query = (
            select(
                func.jsonb_build_object(
                    literal_column("'id'"),
                    cast(model.id, Text),
                    literal_column("'gid'"),
                    cast(model.gid, Text),
                    literal_column("'geometry'"),
                    cast(model.geometry, Text),
                    literal_column("'wkt'"),
                    cast(geo_funcs.ST_AsText(getattr(model, geometry_field)), Text),
                    literal_column("'dma_ids'"),
                    cast(array_agg(dma_alias.id), Text),
                    literal_column("'dma_names'"),
                    cast(array_agg(dma_alias.name), Text),
                    literal_column("'dma_codes'"),
                    cast(array_agg(dma_alias.code), Text),
                    literal_column("'utilities'"),
                    cast(array_agg(utility_alias.name), Text),
                    literal_column("'asset_name'"),
                    cast(literal_column(model.AssetMeta.asset_name), Text),
                ).label("json"),
            )
            .join_from(model, main_dmas_alias, isouter=True)
            .join_from(main_dmas_alias, dma_alias, isouter=True)
            .join_from(dma_alias, utility_alias, isouter=True)
            .where(geo_funcs.ST_Touches(model.geometry, (TrunkMain.geometry)))
            .group_by(
                model.id,
                geo_funcs.ST_AsText(model.geometry),
                geo_funcs.ST_StartPoint(model.geometry),
                geo_funcs.ST_EndPoint(model.geometry),
            )
            .scalar_subquery()
        )

        return array_agg(sub_query)

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
        raise NotImplementedError(
            "Function should be defined in the child class and not called explicitly. "
        )

    def generate_termini_subqueries(self, main_dmas: dict[str, Table]):
        start_point_subqueries: list[Select] = []
        end_point_subqueries: list[Select] = []

        for model in [TrunkMain, DistributionMain]:
            main_dmas_alias = aliased(main_dmas[model.AssetMeta.asset_name])

            subquery_1 = (
                select(
                    model.gid,
                )
                .join_from(model, main_dmas_alias)
                .where(
                    geo_funcs.ST_Touches(
                        model.geometry,
                        geo_funcs.ST_AsText(geo_funcs.ST_StartPoint(model.geometry)),
                    )
                )
            )

            subquery_2 = (
                select(
                    model.gid,
                )
                .join_from(model, main_dmas_alias)
                .where(
                    geo_funcs.ST_Touches(
                        model.geometry,
                        geo_funcs.ST_AsText(geo_funcs.ST_EndPoint(model.geometry)),
                    )
                )
            )

            start_point_subqueries.append(subquery_1)
            end_point_subqueries.append(subquery_2)

        subquery_line_start = (
            start_point_subqueries[0]
            .union(*start_point_subqueries[1:])
            .alias("sq_line_start")
        )
        subquery_line_end = (
            end_point_subqueries[0]
            .union(*end_point_subqueries[1:])
            .alias("sq_line_end")
        )

        return (array_agg(subquery_line_start), array_agg(subquery_line_end))

    def _generate_asset_subqueries(self) -> Any:
        json_fields = self.get_asset_json_fields()
        
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
