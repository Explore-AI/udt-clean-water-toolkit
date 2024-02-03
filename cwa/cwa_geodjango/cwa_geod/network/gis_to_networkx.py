from django.contrib.gis.geos import Point
import networkx as nx
import matplotlib.pyplot as plt
from . import GisToGraph
from cwa_geod.core.constants import DEFAULT_SRID


class GisToNetworkX(GisToGraph):
    """Create a graph network of assets from a geospatial
    network of assets"""

    def __init__(self, srid=None):
        self.srid = srid or DEFAULT_SRID
        self.G = nx.Graph()
        super().__init__(self.srid)

    def create_network(self):
        trunk_mains_nx = self.create_trunk_mains_graph()

        # TODO: geospatial join on all the node assets
        # TODO: add the nodes to the graph

        return trunk_mains_nx

    def create_network2(self):
        trunk_mains_qs = self.get_trunk_mains_data()
        distribution_mains_qs = self.get_distribution_mains_data()

        pipes_qs = trunk_mains_qs.union(distribution_mains_qs, all=True)

        self.calc_pipe_point_relative_positions(pipes_qs)
        self._create_networkx_graph()

    def _set_connected_asset_relations(self, pipe_data, assets_data):
        node_id = f"{pipe_data['asset_id']}-{pipe_data['gisid']}"
        start_of_line_point = Point(pipe_data["geometry"].coords[0][0], srid=27700)

        node_point_geometries = [start_of_line_point]
        new_node_ids = [node_id]

        for asset in assets_data:
            asset_model_name = asset["data"]["asset_model_name"]

            node_type = self._get_node_type(asset_model_name)

            new_asset_id = asset["data"]["id"]
            new_gisid = asset["data"]["gisid"]
            new_node_id = f"{new_asset_id}-{new_gisid}"

            if not self.G.has_node(new_node_id):
                self.G.add_node(
                    new_node_id,
                    position=asset["position"],
                    node_type=node_type,
                    coords=asset["intersection_point_geometry"].coords,
                    **asset["data"],
                )

            edge_length = node_point_geometries[-1].distance(
                asset["intersection_point_geometry"]
            )

            self.G.add_edge(
                new_node_ids[-1],
                new_node_id,
                weight=edge_length,
                asset_id=pipe_data["asset_id"],
                gisid=pipe_data["gisid"],
                normalised_position_on_pipe=asset["position"],
            )
            node_point_geometries.append(asset["intersection_point_geometry"])
            new_node_ids.append(new_node_id)

        # def _map_connected_asset_relations(asset_data):
        #     asset_model_name = asset_data["data"]["asset_model_name"]

        #     node_type = self._get_node_type(asset_model_name)

        #     new_asset_id = asset_data["data"]["id"]
        #     new_gisid = asset_data["data"]["gisid"]
        #     new_node_id = f"{new_asset_id}-{new_gisid}"

        #     if not self.G.has_node(new_node_id):
        #         self.G.add_node(
        #             new_node_id,
        #             position=asset_data["position"],
        #             node_type=node_type,
        #             coords=asset_data["intersection_point_geometry"].coords,
        #             **asset_data["data"],
        #         )

        #     edge_length = node_point_geometries[-1].distance(
        #         asset_data["intersection_point_geometry"]
        #     )

        #     self.G.add_edge(
        #         new_node_ids[-1],
        #         new_node_id,
        #         weight=edge_length,
        #         asset_id=asset_id,
        #         gisid=gisid,
        #         position=asset["position"],
        #     )

        # x = list(map(_map_connected_asset_relations, assets_data))

    def _set_pipe_connected_asset_relations(self):
        def _map_pipe_connected_asset_relations(pipe_data, assets_data):
            node_id = f"{pipe_data['asset_id']}-{pipe_data['gisid']}"

            if not self.G.has_node(node_id):
                self.G.add_node(
                    node_id,
                    coords=pipe_data["geometry"].coords[0][0],
                    **pipe_data,
                )

            self._set_connected_asset_relations(pipe_data, assets_data)

            import pdb

            pdb.set_trace()

        x = list(
            map(
                _map_pipe_connected_asset_relations,
                self.all_pipe_data,
                self.all_asset_positions,
            )
        )

    def _create_networkx_graph(self):
        self._set_pipe_connected_asset_relations()

    def _create_networkx_graph1(self):
        G = nx.Graph()

        pipes_and_assets_position_data = zip(
            self.all_pipe_data, self.all_asset_positions
        )

        for pipe_data, assets_data in pipes_and_assets_position_data:
            asset_id = pipe_data["asset_id"]
            gisid = pipe_data["gisid"]
            start_of_line_point = Point(pipe_data["geometry"].coords[0][0], srid=27700)
            node_id = f"{asset_id}-{gisid}"

            if not G.has_node(node_id):
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

                new_asset_id = asset["data"]["id"]
                new_gisid = asset["data"]["gisid"]
                new_node_id = f"{new_asset_id}-{new_gisid}"

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
                    asset_id=asset_id,
                    gisid=gisid,
                    position=asset["position"],
                )
                node_point_geometries.append(asset["intersection_point_geometry"])
                new_node_ids.append(new_node_id)

        pos = nx.get_node_attributes(G, "coords")
        # https://stackoverflow.com/questions/28372127/add-edge-weights-to-plot-output-in-networkx
        nx.draw(
            G,
            pos=pos,
            node_size=10,
            linewidths=1,
            font_size=15,
        )
        plt.show()

        # use when setting up multiprocessing
        # https://stackoverflow.com/questions/32652149/combine-join-networkx-graphs
        import pdb

        pdb.set_trace()
