import bisect
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
        self._create_graph()

    def _get_connections_points_on_pipe(self, base_pipe_geom, asset_data):
        normalised_positions = []

        for asset in asset_data:
            geom = GEOSGeometry(asset["wkt"], srid=self.srid)

            if geom.geom_typeid in GEOS_LINESTRING_TYPES:
                geom = base_pipe_geom.intersection(
                    geom
                )  # TODO: handle multiple intersection points

            normalised_position_on_pipe = normalised_point_position_on_line(
                base_pipe_geom, geom, srid=self.srid
            )

            bisect.insort(
                normalised_positions,
                {
                    "position": normalised_position_on_pipe,
                    "data": asset,
                    "geometry": geom,
                },
                key=lambda x: x["position"],
            )

        return normalised_positions

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

    def _get_pipe_data(self, qs_object):
        pipe_data = {}
        pipe_data["sql_id"] = qs_object.id
        pipe_data["gisid"] = qs_object.gisid

    def _connect_all_pipes(self, pipes_qs):
        all_asset_positions = []
        all_pipe_data = []

        for pipe_qs_object in pipes_qs[:999]:
            # pipe_positions = self._get_positions_of_pipes_on_pipe(
            #     pipe.geometry, pipe.trunk_mains_data + pipe.distribution_mains_data
            # )

            pipe_data = self._get_pipe_data(pipe_qs_object)
            all_pipe_data.append(pipe_data)

            asset_data = (
                pipe.trunk_mains_data
                + pipe.distribution_mains_data
                + pipe.chamber_data
                + pipe.operational_site_data
                + pipe.network_meter_data
                + pipe.logger_data
                + pipe.hydrant_data
                + pipe.pressure_fitting_data
                + pipe.pressure_valve_data
            )

            asset_positions = self._get_connections_points_on_pipe(
                pipe.geometry, asset_data
            )

            all_asset_positions.append(asset_positions)

        self.all_asset_positions = all_asset_positions

    def _create_graph(self):
        import networkx as nx
        import matplotlib.pyplot as plt

        G = nx.Graph()

        for assets in self.all_asset_positions:
            new_node_ids = []
            # TODO: fix to so that we don't have to do the two loops below
            for asset in assets:
                asset_model_name = asset["data"]["asset_model_name"]

                if asset_model_name in PIPE_ASSETS_MODEL_NAMES:
                    node_type = "pipe_end"
                else:
                    node_type = "point_asset"

                sql_id = asset["data"]["id"]
                gisid = asset["data"]["gisid"]
                node_id = f"{sql_id}-{gisid}"

                new_node_ids.append(node_id)
                if not G.has_node(node_id):
                    G.add_node(
                        node_id,
                        asset_model_name=asset_model_name,
                        node_type=node_type,
                        sql_id=sql_id,
                        gisid=gisid,
                        wkt=asset["data"]["wkt"],
                        sql_dma_id=asset["data"]["dma_id"],
                        dma_code=asset["data"]["dma_code"],
                    )

            # for node in node_ids:
            #     # G.add_edges_from([(1, 2, {'color': 'blue'}), (2, 3, {'weight': 8})])
            #     G.add_edge(
            #         1,
            #         2,
            #         #                weight=assets[0].geometry.length * assets[0]["position"],
            #         data=assets[0]["data"],
            #     )
            # G.add_edge(2, 3, weight=0.1)  # specify edge data
            import pdb

            pdb.set_trace()

        nx.draw(G)
        plt.show()

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

        trunk_mains = tm.get_geometry_queryset()
        return self.create_pipes_network(trunk_mains)
