from django.contrib.gis.geos import GEOSGeometry, Point
from cleanwater.controllers.network_controller import NetworkController
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

    def _get_normalised_point_on_pipe(self, line_geom, point_geom):
        """Get the normalised position of a Point on a pipe relative to the
        pipe start Point. The pipe start Point is the first set of coordinates
        in the tuple returned by geometry.coords where geometry is a
        LineString or MultiLineString
        """

        start_of_pipe_point = Point(line_geom.coords[0][0], srid=self.srid)

        # https://zach.se/geodesic-distance-between-points-in-geodjango/
        # TODO: fix below distane calc as not geodesic
        # https://docs.djangoproject.com/en/5.0/ref/contrib/gis/geos/
        normalised_position_on_pipe1 = 1 - (
            (line_geom.length - start_of_pipe_point.distance(point_geom))
            / line_geom.length
        )

        return normalised_position_on_pipe1

    def _get_positions_of_pipes_on_pipe(self, base_pipe_geom, pipe_data):
        normalised_position_of_pipe_intersections = []

        for pipe in pipe_data:
            geom = GEOSGeometry(pipe["wkt"], srid=self.srid)
            intersection_point = base_pipe_geom.intersection(geom)

            normalised_position_on_pipe = self._get_normalised_point_on_pipe(
                base_pipe_geom, intersection_point
            )
            normalised_position_of_pipe_intersections.append(
                normalised_position_on_pipe
            )

        return normalised_position_of_pipe_intersections

    def _connect_all_pipes(self, pipes_qs):
        i = 0
        for pipe in pipes_qs:
            print(i)
            connected_pipe_positions1 = self._get_positions_of_pipes_on_pipe(
                pipe_geom, pipe.trunk_mains_data
            )

            connected_pipe_positions2 = self._get_positions_of_pipes_on_pipe(
                pipe_geom, pipe.distribution_mains_data
            )

            if i == 200:
                import pdb

                pdb.set_trace()
            i += 1

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
