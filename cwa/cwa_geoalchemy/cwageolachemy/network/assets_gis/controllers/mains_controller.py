from abc import ABC, abstractmethod
from sqlalchemy.dialects.postgresql import array_agg, array
from sqlalchemy.sql import Select, cast
from sqlalchemy import func, select, String, Text, Table, literal_column, text
from sqlalchemy.orm import aliased, Query
from sqlalchemy.sql.expression import literal_column
from geoalchemy2 import functions as geo_funcs
from ..models import *
from cwageolachemy.network.assets_utilities.models import Utility, DMA
from typing import Any, List, Optional, Union


class MainsController(ABC):
    WITHIN_DISTANCE = 0.5
    default_properties = ["id", "gid"]

    def _generate_dwithin_subquery(
        self, model: BaseAsset, asset_dmas, geometry_field="geometry", inner_stmts={}
    ) -> Any:
        tm_touches_subquery = (
            select(TrunkMain.gid)
            .join_from(TrunkMain, trunkmain_dmas, isouter=True)
            .where(
                geo_funcs.ST_DWithin(
                    TrunkMain.geometry, model.geometry, self.WITHIN_DISTANCE
                )
            )
            .order_by(trunkmain_dmas.c.dma_id.asc())
            .limit(20)
            .scalar_subquery()
            .label("trunkmain_touches")
        )

        dm_touches_subquery = (
            select(DistributionMain.gid)
            .join_from(DistributionMain, distributionmain_dmas, isouter=True)
            .where(
                geo_funcs.ST_DWithin(
                    DistributionMain.geometry, model.geometry, self.WITHIN_DISTANCE
                )
            )
            .order_by(distributionmain_dmas.c.dma_id.asc())
            .scalar_subquery()
            .label("distributionmain_touches")
        )

        dwithin_asset_subquery = (
            select(
                func.jsonb_build_object(
                    literal_column("'id'"),
                    cast(model.id, Text),
                    literal_column("'gid'"),
                    cast(model.gid, Text),
                    literal_column("'geometry'"),
                    cast(model.geometry, Text),
                    literal_column("'wkt'"),
                    cast(geo_funcs.ST_AsText(model.geometry), Text),
                    literal_column("'dma_ids'"),
                    cast(array_agg(DMA.id), Text),
                    literal_column("'dma_names'"),
                    cast(array_agg(DMA.name), Text),
                    literal_column("'dma_codes'"),
                    cast(array_agg(DMA.code), Text),
                    literal_column("'utilities'"),
                    cast(array_agg(Utility.name), Text),
                    literal_column("'tm_touches_gids'"),
                    array_agg(tm_touches_subquery),
                    literal_column("'dm_touches_gids'"),
                    array_agg(dm_touches_subquery),
                )
            )
            .join_from(model, asset_dmas, isouter=True)
            .join_from(asset_dmas, DMA, isouter=True)
            .join_from(DMA, Utility, isouter=True)
            .where(geo_funcs.ST_DWithin(model.geometry, (TrunkMain.geometry), 0.5))
            .group_by(
                model.id,
                geo_funcs.ST_AsText(model.geometry),
            )
            .scalar_subquery()
        )

        return dwithin_asset_subquery

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
            .scalar_subquery()
            .alias("line_start_intersection_gids")
        )
        subquery_line_end = (
            end_point_subqueries[0]
            .union(*end_point_subqueries[1:])
            .scalar_subquery()
            .alias("line_end_intersection_gids")
        )

        return (subquery_line_start, subquery_line_end)

    def _generate_asset_subqueries(self) -> Any:
        logger_subquery = self._generate_dwithin_subquery(Logger, logger_dmas)
        hydrant_subquery = self._generate_dwithin_subquery(Hydrant, hydrant_dmas)
        pressure_fitting_subquery = self._generate_dwithin_subquery(
            PressureFitting, pressurefitting_dmas
        )
        pressure_valve_subquery = self._generate_dwithin_subquery(
            PressureControlValve, pressurecontrolvalve_dmas
        )
        network_meter_subquery = self._generate_dwithin_subquery(
            NetworkMeter, networkmeter_dmas
        )
        chamber_subquery = self._generate_dwithin_subquery(Chamber, chamber_dmas)
        operational_site_subquery = self._generate_dwithin_subquery(
            OperationalSite, operationalsite_dmas
        )
        network_opt_valve_subquery = self._generate_dwithin_subquery(
            NetworkOptValve, networkoptvalve_dmas
        )

        return {
            "loggers": logger_subquery,
            "hydrants": hydrant_subquery,
            "pressure_fittings": pressure_fitting_subquery,
            "pressure_valve": pressure_valve_subquery,
            "network_meters": network_meter_subquery,
            "chambers": chamber_subquery,
            "operational_sites": operational_site_subquery,
            "network_opt_valve": network_opt_valve_subquery,
        }

        # return {
        #     "loggers": logger_subquery.label("logger_data"),
        #     "hydrants": hydrant_subquery.label("hydrants_data"),
        #     "pressure_fittings": pressure_fitting_subquery.label("pressure_fitting_data"),
        #     "pressure_valve": pressure_valve_subquery.label("pressure_valve_data"),
        #     "network_meters": network_meter_subquery.label("network_meter_data"),
        #     "chambers": chamber_subquery.label("chamber_data"),
        #     "operational_sites": operational_site_subquery.label("operational_site_data"),
        #     "network_opt_valve": network_opt_valve_subquery.label("network_opt_valve_data"),
        # }

    def get_pipe_point_relation_queryset(
        self, model: Union[DistributionMain, TrunkMain], main_dmas: Table
    ) -> Any:

        utility_alias = aliased(Utility)
        dma_alias = aliased(DMA)
        # get our subqueries
        mains_intersection_stmt = self._generate_mains_subqueries()
        asset_stmt = self._generate_asset_subqueries()
        asset_name = model.AssetMeta.asset_name
        # add the subqueries to the main query
        point_relation_query = (
            select(
                model.id,
                model.gid,
                model.geometry,
                model.modified_at,
                model.created_at,
                literal_column(asset_name).label("asset_name"),
                geo_funcs.ST_AsText(geo_funcs.ST_Length(model.geometry)).label(
                    "pipe_length"
                ),
                geo_funcs.ST_AsText(model.geometry).label("wkt"),
                array_agg(main_dmas.c.dma_id).label("dma_ids"),
                array_agg(dma_alias.code).label("dma_codes"),
                array_agg(dma_alias.name).label("dma_names"),
                geo_funcs.ST_AsText(geo_funcs.ST_StartPoint(model.geometry)).label(
                    "start_point_geom"
                ),
                geo_funcs.ST_AsText(geo_funcs.ST_EndPoint(model.geometry)).label(
                    "end_point_geom"
                ),
                array_agg(utility_alias.name).label("utility_names"),
                mains_intersection_stmt["trunkmain_junctions"],
                mains_intersection_stmt["distmain_junctions"],
                array_agg(
                    mains_intersection_stmt["line_start_intersection_gids"]
                ).label("line_start_intersection_gids"),
                array_agg(mains_intersection_stmt["line_end_intersection_gids"]).label(
                    "line_end_intersection_gids"
                ),
                array_agg(asset_stmt["loggers"]).label("logger_data"),
                array_agg(asset_stmt["hydrants"]).label("hydrant_data"),
                array_agg(asset_stmt["pressure_fittings"]).label(
                    "pressure_fitting_data"
                ),
                array_agg(asset_stmt["pressure_valve"]).label("pressure_valve_data"),
                array_agg(asset_stmt["network_meters"]).label("network_meter_data"),
                array_agg(asset_stmt["chambers"]).label("chamber_data"),
                array_agg(asset_stmt["operational_sites"]).label(
                    "operational_site_data"
                ),
                array_agg(asset_stmt["network_opt_valve"]).label(
                    "network_opt_valve_data"
                ),
            )
            .join_from(model, main_dmas, isouter=True)
            .join_from(main_dmas, dma_alias, isouter=True)
            .join_from(dma_alias, utility_alias, isouter=True)
            .where(dma_alias.code.in_(["ZWAL4801", "ZCHESS12", "ZCHIPO01"]))
            .group_by(dma_alias.id)
        )
        print(f"Point Relation query: {point_relation_query}")

    def get_geometry_queryset(self) -> Any:
        pass

    def mains_to_geojson(self, properties=None) -> Any:
        pass

    def mains_to_geojson2(self, properties=None) -> Any:
        pass

    def mains_to_geodataframe(self, properties=None) -> Any:
        pass
