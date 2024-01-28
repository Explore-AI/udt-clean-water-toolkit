import bisect
from django.contrib.gis.geos import GEOSGeometry
from cleanwater.controllers.network_controller import NetworkController
from cleanwater.core.utils import normalised_point_position_on_line
from cwa_geod.assets.controllers import TrunkMainsController
from cwa_geod.assets.controllers import DistributionMainsController
from cwa_geod.config.settings import DEFAULT_SRID


class GisToGraphNetwork(NetworkController):
    """Create a graph network of assets from a geospatial
    network of assets"""

    def __init__(self, srid=None):
        self.srid = srid or DEFAULT_SRID
        super().__init__(self.srid)

    def create_network(self):
        trunk_mains_nx = self._create_trunk_mains_graph()

        # TODO: geospatial join on all the node assets
        # TODO: add the nodes to the graph

        return trunk_mains_nx

    def create_network2(self):
        trunk_mains_qs = self._get_trunk_mains_data()
        distribution_mains_qs = self._get_distribution_mains_data()

        pipes_qs = trunk_mains_qs.union(distribution_mains_qs, all=True)

        self._connect_all_pipes(pipes_qs)

    def _get_positions_of_pipes_on_pipe(self, base_pipe_geom, pipe_data):
        normalised_positions = []

        for pipe in pipe_data:
            geom = GEOSGeometry(pipe["wkt"], srid=self.srid)
            intersection_point = base_pipe_geom.intersection(
                geom
            )  # TODO: handle multiple intersection points

            normalised_position_on_pipe = normalised_point_position_on_line(
                base_pipe_geom, intersection_point, srid=self.srid
            )

            bisect.insort(
                normalised_positions,
                {"position": normalised_position_on_pipe, "data": pipe},
                key=lambda x: x["position"],
            )

        return normalised_positions

    def _get_positions_of_points_on_pipe(self, base_pipe_geom, point_data):
        normalised_positions = []

        for point in point_data:
            geom = GEOSGeometry(point["wkt"], srid=self.srid)

            normalised_position_on_pipe = normalised_point_position_on_line(
                base_pipe_geom, geom, srid=self.srid
            )

            bisect.insort(
                normalised_positions,
                {"position": normalised_position_on_pipe, "data": point},
                key=lambda x: x["position"],
            )

        return normalised_positions

    def _connect_all_pipes(self, pipes_qs):
        point_pipe_positions = []
        for pipe in pipes_qs[:999]:
            pipe_positions = self._get_positions_of_pipes_on_pipe(
                pipe.geometry, pipe.trunk_mains_data + pipe.distribution_mains_data
            )

            point_pipe_positions.append(pipe_positions)

        import pdb

        pdb.set_trace()

    def _get_trunk_mains_data(self):
        tm = TrunkMainsController()
        return tm.get_pipe_point_relation_queryset()

    def _get_distribution_mains_data(self):
        dm = DistributionMainsController()
        return dm.get_pipe_point_relation_queryset()

    def _create_trunk_mains_graph(self):
        tm = TrunkMainsController()

        # TODO: union querysets
        # dm = DistributionMainsController()

        trunk_mains = tm.get_geometry_queryset()
        return self.create_pipes_network(trunk_mains)
