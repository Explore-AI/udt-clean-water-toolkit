from cwageolachemy.network.assets_gis.controllers.trunk_mains_controller import (
    TrunkMainsController,
)
from ...assets_gis.controllers.distribution_mains_controller import (
    DistributionMainsController,
)
from cwageolachemy.network.assets_gis.models import *
from cwageolachemy.network.assets_utilities.models import *
from sqlalchemy.orm import Session
from sqlalchemy import select, func, Integer, Row
from sqlalchemy.dialects.postgresql import array_agg, array, ARRAY, JSONB
from cwageolachemy.config.db_config import engine
from sqlalchemy.orm import aliased, Query, joinedload
import json


class GisToNeo4jController:
    def __init__(self) -> None:
        pass

    def create_network(self):
        pipes_query = self._get_pipe_and_asset_data()

        with Session(engine) as session:
            count = 0
            query_result = session.execute(select("*").select_from(pipes_query))
            for pipe_data in query_result:
                pipe_data_as_dict = pipe_data._asdict()
                base_pipe_data = self._get_base_pipe_data(pipe_data_as_dict)
                junctions_data = self._combine_all_pipe_junctions(pipe_data_as_dict)
                assets_data = self._combine_all_point_assets(pipe_data_as_dict)

    def _get_pipe_and_asset_data(self):
        trunk_mains_statement = self.get_trunk_mains_data()
        distribution_mains_statement = self.get_distribution_mains_data()

        unioned_query = trunk_mains_statement.union_all(distribution_mains_statement)

        return unioned_query

    def get_trunk_mains_data(self):
        tm: TrunkMainsController = TrunkMainsController()
        return tm.get_pipe_point_relation_queryset(
            model=TrunkMain, main_dmas=trunkmain_dmas
        )

    def get_distribution_mains_data(self):
        dm: DistributionMainsController = DistributionMainsController()
        return dm.get_pipe_point_relation_queryset(
            model=DistributionMain, main_dmas=distributionmain_dmas
        )

    def _get_base_pipe_data(self, row_data: dict) -> dict:
        # take the expected fields from the db
        base_pipe = {
            "id": row_data["id"],
            "gid": row_data["gid"],
            "geometry": row_data["geometry"],
            "modified_at": row_data["modified_at"],
            "created_at": row_data["created_at"],
            "asset_name": row_data["asset_name"],
            "pipe_length": row_data["pipe_length"],
            "wkt": row_data["wkt"],
            "dma_ids": row_data["dma_ids"],
            "dma_codes": row_data["dma_codes"],
            "dma_names": row_data["dma_names"],
            "dmas": self.build_dma_data_as_json(
                row_data["dma_codes"], row_data["dma_names"]
            ),
            "start_point_geom": row_data["start_point_geom"],
            "end_point_geom": row_data["end_point_geom"],
            "utility_names": row_data["utility_names"],
            "line_start_intersections_gids": row_data["line_start_intersections"][0][
                "gids"
            ],
            "line_end_intersections_gids": row_data["line_end_intersections"][0][
                "gids"
            ],
            "line_start_intersections_ids": row_data["line_start_intersections"][0][
                "ids"
            ],
            "line_end_intersections_ids": row_data["line_end_intersections"][0]["ids"],
        }
        return base_pipe

    def _combine_all_pipe_junctions(self, row_data: dict) -> list:
        return [row_data["trunkmain_junctions"], row_data["distmain_junctions"]]

    def _combine_all_point_assets(self, row_data: dict) -> list:
        assets = [
            "logger_data",
            "hydrant_data",
            "pressure_fitting_data",
            "network_meter_data",
            "chamber_data",
            "operational_site_data",
            "network_opt_valve_data",
        ]

        asset_data = []
        for asset in assets:
            if asset in row_data.keys():
                asset_data.append(row_data[asset])

        return asset_data

    @staticmethod
    def build_dma_data_as_json(dma_codes, dma_names):
        dma_data = [
            {"code": dma_code, "name": dma_name}
            for dma_code, dma_name in zip(dma_codes, dma_names)
        ]

        return json.dumps(dma_data)

    @staticmethod
    def _get_utility():
        pass
