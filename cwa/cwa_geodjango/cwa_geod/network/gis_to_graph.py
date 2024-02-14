import bisect
import multiprocessing as mp
from django.contrib.gis.geos import GEOSGeometry
from cleanwater.controllers.network_controller import NetworkController
from cleanwater.core.utils import normalised_point_position_on_line
from cwa_geod.assets.controllers import TrunkMainsController
from cwa_geod.assets.controllers import DistributionMainsController
from cwa_geod.core.constants import (
    DEFAULT_SRID,
    PIPE_ASSETS_MODEL_NAMES,
    GEOS_LINESTRING_TYPES,
)


class GisToGraph(NetworkController):
    def __init__(self, srid=None):
        self.srid = srid or DEFAULT_SRID
        super().__init__(self.srid)

    def _get_connections_points_on_pipe(self, base_pipe_geom, asset_data):
        normalised_positions = []

        for asset in asset_data:
            geom = GEOSGeometry(asset["wkt"], srid=self.srid)

            if geom.geom_typeid in GEOS_LINESTRING_TYPES:
                geom = base_pipe_geom.intersection(
                    geom
                )  # TODO: handle multiple intersections at single point

            normalised_position_on_pipe = normalised_point_position_on_line(
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

    def _get_pipe_data(self, qs_object):
        pipe_data = {}
        pipe_data["asset_id"] = qs_object.id
        pipe_data["gisid"] = qs_object.gisid
        pipe_data["asset_model_name"] = qs_object.asset_model_name
        pipe_data["length"] = qs_object.length
        pipe_data["shape_length"] = qs_object.shape_length
        pipe_data["wkt"] = qs_object.wkt
        pipe_data["dma_code"] = qs_object.dma.code
        pipe_data["dma_id"] = qs_object.dma_id
        pipe_data["geometry"] = qs_object.geometry

        return pipe_data

    def _combine_all_asset_data(self, pipe_qs_object):
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

    def _map_relative_positions_calc(self, pipe_qs_object):
        pipe_data = self._get_pipe_data(pipe_qs_object)
        asset_data = self._combine_all_asset_data(pipe_qs_object)

        asset_positions = self._get_connections_points_on_pipe(
            pipe_qs_object.geometry, asset_data
        )

        return pipe_data, asset_positions

    def calc_pipe_point_relative_positions(self, pipes_qs):
        from timeit import default_timer as timer

        start = timer()
        # TODO: fix slice approach
        self.all_pipe_data, self.all_asset_positions = list(
            zip(*map(self._map_relative_positions_calc, pipes_qs[:1000]))
        )
        end = timer()
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

    def _get_node_type(self, asset_model_name):
        if asset_model_name in PIPE_ASSETS_MODEL_NAMES:
            return "pipe_end"

        return "point_asset"

    def get_trunk_mains_data(self):
        tm = TrunkMainsController()
        return tm.get_pipe_point_relation_queryset()

    def get_distribution_mains_data(self):
        dm = DistributionMainsController()
        return dm.get_pipe_point_relation_queryset()

    def create_trunk_mains_graph(self):
        tm: TrunkMainsController = TrunkMainsController()

        trunk_mains = tm.get_geometry_queryset()
        # import pdb; pdb.set_trace()
        return self.create_pipes_network(trunk_mains)
