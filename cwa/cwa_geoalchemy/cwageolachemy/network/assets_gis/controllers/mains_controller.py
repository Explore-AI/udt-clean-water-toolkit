from abc import ABC, abstractmethod
from sqlalchemy.dialects.postgresql import array_agg, array
from sqlalchemy.sql import Select, cast
from sqlalchemy import (
    func,
    select,
    String,
    Text,
    Table,
    literal_column,
    text,
    union_all,
)
from sqlalchemy.orm import aliased, Query, joinedload
from sqlalchemy.sql.expression import literal_column, literal
from geoalchemy2 import functions as geo_funcs
from ..models import *
from cwageolachemy.network.assets_utilities.models import Utility, DMA
from typing import Any, List, Optional, Union
from cwageolachemy.config.db_config import engine
from sqlalchemy.orm import Session


class MainsController(ABC):
    WITHIN_DISTANCE = 0.5
    default_properties = ["id", "gid"]

    def _generate_dwithin_subquery(
        self, model: BaseAsset, asset_dmas, geometry_field="geometry", inner_stmts={}
    ) -> Any:
        # trunkmain_dma_alias = aliased(trunkmain_dmas)
        # distmain_dma_alias = aliased(distributionmain_dmas)
        asset_name = model.AssetMeta.asset_name
        
        tm_touches_subquery = (
            select(TrunkMain.id)
            .join_from(
                trunkmain_dmas, model, trunkmain_dmas.c.dma_id == asset_dmas.c.dma_id
            )
            .where(
                geo_funcs.ST_DWithin(
                    TrunkMain.geometry, model.geometry, self.WITHIN_DISTANCE
                )
            )
            .order_by(trunkmain_dmas.c.dma_id.asc())
            .limit(1)
            .scalar_subquery()
        )

        dm_touches_subquery = (
            select(DistributionMain.id)
            .join_from(
                distributionmain_dmas,
                model,
                distributionmain_dmas.c.dma_id == asset_dmas.c.dma_id,
            )
            .where(
                geo_funcs.ST_DWithin(
                    DistributionMain.geometry, model.geometry, self.WITHIN_DISTANCE
                )
            )
            .order_by(distributionmain_dmas.c.dma_id.asc())
            .limit(1)
            .scalar_subquery()
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
                    literal_column("'tm_touches_ids'"),
                    array_agg(tm_touches_subquery),
                    literal_column("'dm_touches_ids'"),
                    array_agg(dm_touches_subquery),
                    literal_column("'asset_name'"), 
                    asset_name
                ).label("json")
            )
            .join_from(model, asset_dmas, isouter=True)
            .join_from(asset_dmas, DMA, isouter=True)
            .join_from(DMA, Utility, isouter=True)
            .where(geo_funcs.ST_DWithin(model.geometry, (TrunkMain.geometry), 0.5))
            .group_by(
                model.id,
                geo_funcs.ST_AsText(model.geometry),
            )
            .limit(1)
            .subquery()
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
                    cast(literal(model.AssetMeta.asset_name), Text).label("asset_name"),
                ).label("json"),
            )
            .join_from(model, main_dmas_alias, isouter=True)
            .join_from(main_dmas_alias, dma_alias, isouter=True)
            .join_from(dma_alias, utility_alias, isouter=True)
            .limit(1)
            .where(
                geo_funcs.ST_Touches(
                    model.geometry, (geo_funcs.ST_Transform(TrunkMain.geometry, 27700))
                )
            )
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
        raise NotImplementedError(
            "Function should be defined in the child class and not called explicitly. "
        )

    def generate_termini_subqueries(self, main_dmas: dict[str, Table]):
        start_point_subqueries: list[Select] = []
        end_point_subqueries: list[Select] = []
        tm_alias = aliased(TrunkMain)
        dm_alias = aliased(DistributionMain)
        # Get TrunkMain queries
        tm_subquery_1 = (
            select(
                func.jsonb_build_object(
                    literal_column("'ids'"),
                    array_agg(tm_alias.id),
                    literal_column("'gids'"),
                    array_agg(tm_alias.gid),
                ).label("json")
            )
            .join_from(tm_alias, main_dmas["trunk_main"], isouter=True)
            .where(
                geo_funcs.ST_Touches(
                    tm_alias.geometry,
                    geo_funcs.ST_Transform(
                        geo_funcs.ST_StartPoint(TrunkMain.geometry), 27700
                    ),
                )
            )
            .group_by(tm_alias.id)
        )

        tm_subquery_2 = (
            select(
                func.jsonb_build_object(
                    literal_column("'ids'"),
                    array_agg(tm_alias.id),
                    literal_column("'gids'"),
                    array_agg(tm_alias.gid),
                ).label("json")
            )
            .join_from(tm_alias, main_dmas["trunk_main"], isouter=True)
            .where(
                geo_funcs.ST_Touches(
                    tm_alias.geometry,
                    geo_funcs.ST_Transform(
                        geo_funcs.ST_EndPoint(TrunkMain.geometry), 27700
                    ),
                )
            )
            .group_by(TrunkMain.id)
        )

        # Get DistMain queries
        dm_subquery_1 = (
            select(
                func.jsonb_build_object(
                    literal_column("'ids'"),
                    array_agg(dm_alias.id),
                    literal_column("'gids'"),
                    array_agg(dm_alias.gid),
                ).label("json")
            )
            .join_from(dm_alias, main_dmas["distribution_main"], isouter=True)
            .where(
                geo_funcs.ST_Touches(
                    dm_alias.geometry,
                    geo_funcs.ST_Transform(
                        geo_funcs.ST_StartPoint(DistributionMain.geometry), 27700
                    ),
                )
            )
            .group_by(dm_alias.id)
        )
        dm_subquery_2 = (
            select(
                func.jsonb_build_object(
                    literal_column("'ids'"),
                    array_agg(dm_alias.id),
                    literal_column("'gids'"),
                    array_agg(dm_alias.gid),
                ).label("json")
            )
            .join_from(dm_alias, main_dmas["distribution_main"], isouter=True)
            .where(
                geo_funcs.ST_Touches(
                    dm_alias.geometry,
                    geo_funcs.ST_Transform(
                        geo_funcs.ST_EndPoint(DistributionMain.geometry), 27700
                    ),
                )
            )
            .group_by(dm_alias.id)
        )

        start_point_subqueries = [tm_subquery_1, dm_subquery_1]
        end_point_subqueries = [tm_subquery_2, dm_subquery_2]

        subquery_line_start = (
            union_all(
                start_point_subqueries[0], *start_point_subqueries[1:]
            )
            .limit(1)
            .subquery()
        )
        subquery_line_end = (
            union_all(
                end_point_subqueries[0], *end_point_subqueries[1:]
            )
            .limit(1)
            .subquery()
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

    def get_pipe_point_relation_queryset(
        self, model: Union[DistributionMain, TrunkMain], main_dmas: Table
    ) -> Select:

        uu_alias = aliased(Utility)  # utilities utility
        ud_alias = aliased(DMA)  # utilities dma
        # get our subqueries
        mains_intersection_stmt = self._generate_mains_subqueries()
        asset_stmt = self._generate_asset_subqueries()
        asset_name = model.AssetMeta.asset_name
        # add the subqueries to the main query
        point_relation_query = (
            select(
                model.id,
                model.gid,
                geo_funcs.ST_AsText(model.geometry),
                model.modified_at,
                model.created_at,
                literal(asset_name).label("asset_name"),
                geo_funcs.ST_Length(model.geometry).label("pipe_length"),
                geo_funcs.ST_AsText(model.geometry).label("wkt"),
                array_agg(main_dmas.c.dma_id).label("dma_ids"),
                array_agg(ud_alias.code).label("dma_codes"),
                array_agg(ud_alias.name).label("dma_names"),
                geo_funcs.ST_AsText(geo_funcs.ST_StartPoint(model.geometry)).label(
                    "start_point_geom"
                ),
                geo_funcs.ST_AsText(geo_funcs.ST_EndPoint(model.geometry)).label(
                    "end_point_geom"
                ),
                array_agg(uu_alias.name).label("utility_names"),
                array_agg(mains_intersection_stmt["trunkmain_junctions"]).label(
                    "trunkmain_junctions"
                ),
                array_agg(mains_intersection_stmt["distmain_junctions"]).label(
                    "distmain_junctions"
                ),
                array_agg(
                    mains_intersection_stmt["line_start_intersection_gids"].c.json
                ).label("line_start_intersections"),
                array_agg(mains_intersection_stmt["line_end_intersection_gids"].c.json).label("line_end_intersections"),
                array_agg(asset_stmt["loggers"].c.json).label("logger_data"),
                array_agg(asset_stmt["hydrants"].c.json).label("hydrant_data"),
                array_agg(asset_stmt["pressure_fittings"].c.json).label(
                    "pressure_fitting_data"
                ),
                array_agg(asset_stmt["pressure_valve"].c.json).label("pressure_valve_data"),
                array_agg(asset_stmt["network_meters"].c.json).label("network_meter_data"),
                array_agg(asset_stmt["chambers"].c.json).label("chamber_data"),
                array_agg(asset_stmt["operational_sites"].c.json).label(
                    "operational_site_data"
                ),
                array_agg(asset_stmt["network_opt_valve"].c.json).label(
                    "network_opt_valve_data"
                ),
            )
            # .options(joinedload(model.dmas))
            .join_from(model, main_dmas)
            .join_from(main_dmas, ud_alias)
            .join_from(ud_alias, uu_alias)
            .where(DMA.code.in_(["ZWAL4801", "ZCHESS12"]))
            .offset(50)
            .limit(20)
            .group_by(model.id)
        )
        return point_relation_query

    def get_geometry_queryset(self) -> Any:
        pass

    def mains_to_geojson(self, properties=None) -> Any:
        pass

    def mains_to_geojson2(self, properties=None) -> Any:
        pass

    def mains_to_geodataframe(self, properties=None) -> Any:
        pass
