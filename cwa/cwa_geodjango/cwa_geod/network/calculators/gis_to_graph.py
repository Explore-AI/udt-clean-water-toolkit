import bisect
import multiprocessing as mp
from networkx import Graph
from django.contrib.gis.geos import GEOSGeometry, MultiLineString
from django.db.models.query import QuerySet
from cleanwater.controllers.network_controller import NetworkController
from cleanwater.core.utils import normalised_point_position_on_line
from cwa_geod.assets.controllers import TrunkMainsController
from cwa_geod.assets.models.trunk_main import TrunkMain
from cwa_geod.assets.controllers import DistributionMainsController
from cwa_geod.core.constants import (
    DEFAULT_SRID,
    PIPE_ASSETS__NAMES,
    GEOS_LINESTRING_TYPES,
)


class GisToGraph(NetworkController):
    def __init__(self, srid=None):
        self.srid = srid or DEFAULT_SRID
        super().__init__(self.srid)

    def _get_connections_points_on_pipe(
        self, base_pipe_geom: MultiLineString, asset_data: list
    ) -> list:
        normalised_positions: list = []

        for asset in asset_data:
            geom: MultiLineString = GEOSGeometry(asset["wkt"], srid=self.srid)

            if geom.geom_typeid in GEOS_LINESTRING_TYPES:
                geom = base_pipe_geom.intersection(
                    geom
                )  # TODO: handle multiple intersections at single point

            normalised_position_on_pipe: float = normalised_point_position_on_line(
                base_pipe_geom, geom, srid=self.srid
            )

            bisect.insort(
                normalised_positions,
                {
                    "position": normalised_position_on_pipe,
                    "data": asset,
                    "intersection_point_geometry": geom,
                },
                key=lambda x: x["position"],
            )
        return normalised_positions

    def _get_pipe_data(self, qs_object: TrunkMain) -> dict:
        pipe_data: dict = {}
        pipe_data["id"] = qs_object.id
        pipe_data["gid"] = qs_object.gid
        pipe_data["asset_name"] = qs_object.asset_name
        pipe_data["length"] = qs_object.length
        pipe_data["wkt"] = qs_object.wkt
        pipe_data["dma_ids"] = list(qs_object.dmas.values_list("id", flat=True))
        pipe_data["dma_codes"] = list(qs_object.dmas.values_list("code", flat=True))
        pipe_data["dma_names"] = list(qs_object.dmas.values_list("name", flat=True))
        pipe_data["geometry"] = qs_object.geometry

        return pipe_data

    def _combine_all_asset_data(self, pipe_qs_object: TrunkMain) -> list:
        return (
            pipe_qs_object.trunk_mains_data
            + pipe_qs_object.distribution_mains_data
            + pipe_qs_object.chamber_data
            + pipe_qs_object.operational_site_data
            + pipe_qs_object.network_meter_data
            + pipe_qs_object.logger_data
            + pipe_qs_object.hydrant_data
            + pipe_qs_object.pressure_fitting_data
            + pipe_qs_object.pressure_valve_data
        )

    def _map_relative_positions_calc(
        self, pipe_qs_object: TrunkMain
    ) -> tuple[dict, list]:
        pipe_data: dict = self._get_pipe_data(pipe_qs_object)
        asset_data: list = self._combine_all_asset_data(pipe_qs_object)

        asset_positions: list = self._get_connections_points_on_pipe(
            pipe_qs_object.geometry, asset_data
        )
        return pipe_data, asset_positions

    def calc_pipe_point_relative_positions(self, pipes_qs: QuerySet) -> None:
        from timeit import default_timer as timer

        start: float = timer()
        # TODO: fix slice approach
        self.all_pipe_data, self.all_asset_positions = list(
            zip(*map(self._map_relative_positions_calc, pipes_qs[:100]))
        )
        end: float = timer()
        print(end - start)

        # start = timer()

        # qs_list = [
        #     pipes_qs[:1000],
        #     pipes_qs[1000:2000],
        #     pipes_qs[2000:3000],
        #     pipes_qs[3000:4000],
        # ]
        # with mp.Pool(4) as pool:
        #     self.all_pipe_data, self.all_asset_positions = list(
        #         zip(*pool.map(self._map_relative_positions_calc, qs_list))
        #     )

        # end = timer()
        # print(end - start)

    @staticmethod
    def _get_node_type(asset_name: str) -> str:
        if asset_name in dict(PIPE_ASSETS__NAMES).keys():
            return "pipe_end"

        return "point_asset"

    def get_trunk_mains_data(self) -> QuerySet:
        tm: TrunkMainsController = TrunkMainsController()
        return tm.get_pipe_point_relation_queryset()

    def get_distribution_mains_data(self) -> QuerySet:
        dm: DistributionMainsController = DistributionMainsController()
        return dm.get_pipe_point_relation_queryset()

    # TODO: remove from here as it contains specific nx methods
    def create_trunk_mains_graph(self) -> Graph:
        tm: TrunkMainsController = TrunkMainsController()

        trunk_mains: QuerySet = tm.get_geometry_queryset()
        return self.create_pipes_network(trunk_mains)

    def set_srid(self, srid: int):
        """Set or change the global srid"""
        self.srid = srid

    def get_srid(self):
        """Get the currently used global srid"""
        return self.srid
