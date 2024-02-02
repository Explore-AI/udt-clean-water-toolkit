import bisect
from django.contrib.gis.geos import GEOSGeometry, Point
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
        pipe_data["asset_model_name"] = qs_object.asset_model_name
        pipe_data["length"] = qs_object.length
        pipe_data["shape_length"] = qs_object.shape_length
        pipe_data["wkt"] = qs_object.wkt
        pipe_data["dma_code"] = qs_object.dma.code
        pipe_data["dma_id"] = qs_object.dma_id
        pipe_data["geometry"] = qs_object.geometry

        return pipe_data

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

            asset_positions = self._get_connections_points_on_pipe(
                pipe_qs_object.geometry, asset_data
            )

            all_asset_positions.append(asset_positions)

        self.all_asset_positions = all_asset_positions
        self.all_pipe_data = all_pipe_data

    def _get_node_type(self, asset_model_name):
        if asset_model_name in PIPE_ASSETS_MODEL_NAMES:
            return "pipe_end"

        return "point_asset"

    def _create_graph(self):
        import networkx as nx
        import matplotlib.pyplot as plt

        G = nx.Graph()

        pipes_and_assets_position_data = zip(
            self.all_pipe_data, self.all_asset_positions
        )

        for pipe_data, assets_data in pipes_and_assets_position_data:
            sql_id = pipe_data["sql_id"]
            gisid = pipe_data["gisid"]
            start_of_line_point = Point(pipe_data["geometry"].coords[0][0], srid=27700)
            node_id = f"{sql_id}-{gisid}"

            if not G.has_node(node_id):
                print("sdfsdfs", node_id)
                G.add_node(
                    node_id,
                    coords=pipe_data["geometry"].coords[0][0],
                    **pipe_data,
                )

            node_point_geometries = [start_of_line_point]
            new_node_ids = [node_id]

            # TODO: fix so that we don't have to do the two loops below
            for asset in assets_data:
                asset_model_name = asset["data"]["asset_model_name"]

                node_type = self._get_node_type(asset_model_name)

                new_sql_id = asset["data"]["id"]
                new_gisid = asset["data"]["gisid"]
                new_node_id = f"{new_sql_id}-{new_gisid}"

                if not G.has_node(new_node_id):
                    G.add_node(
                        new_node_id,
                        position=asset["position"],
                        node_type=node_type,
                        coords=asset["intersection_point_geometry"].coords,
                        **asset["data"],
                    )

                edge_length = node_point_geometries[-1].distance(
                    asset["intersection_point_geometry"]
                )

                G.add_edge(
                    new_node_ids[-1],
                    new_node_id,
                    weight=edge_length,
                    sql_id=sql_id,
                    gisid=gisid,
                    position=asset["position"],
                )
                node_point_geometries.append(asset["intersection_point_geometry"])
                new_node_ids.append(new_node_id)

            print(G.edges)
            print(G.nodes)

            pos = nx.get_node_attributes(G, "coords")
            nx.draw(
                G,
                pos=pos,
                # with_labels=True,
                # node_color="blue",
                node_size=100,
                # edge_color="black",
                linewidths=1,
                font_size=15,
            )
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
