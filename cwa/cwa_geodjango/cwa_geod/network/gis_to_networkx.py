from django.contrib.gis.geos import Point
from typing import Any, Dict, List
# import networkx as nx
from networkx import Graph
import matplotlib.pyplot as plt
from . import GisToGraph
from cwa_geod.core.constants import DEFAULT_SRID


class GisToNetworkX(GisToGraph):
    """Create a NetworkX graph of assets from a geospatial
    network of assets"""

    def __init__(self, srid: int) -> None:
        # self.srid = srid or DEFAULT_SRID
        self.srid: int = srid or DEFAULT_SRID
        # self.G = nx.Graph()
        self.G: Graph = Graph()
        super().__init__(self.srid)

    def create_network(self) -> Graph:
        trunk_mains_nx: Graph = self.create_trunk_mains_graph()

        # TODO: geospatial join on all the node assets
        # TODO: add the nodes to the graph
        # import pdb; pdb.set_trace()
        # return trunk_mains_nx

    # def create_network2(self) -> nx.Graph:
    def create_network2(self) -> Graph:
        trunk_mains_qs = self.get_trunk_mains_data()
        distribution_mains_qs = self.get_distribution_mains_data()

        pipes_qs = trunk_mains_qs.union(distribution_mains_qs, all=True)

        self.calc_pipe_point_relative_positions(pipes_qs)
        self._create_networkx_graph()
        return self.G

    def _set_connected_asset_relations(
        self, pipe_data: Dict[str, Any], assets_data: List[Dict[str, Any]]
    ) -> None:
        node_id = f"{pipe_data['asset_id']}-{pipe_data['gisid']}"
        start_of_line_point = Point(
            pipe_data["geometry"].coords[0][0], srid=DEFAULT_SRID
        )

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

    def _set_pipe_connected_asset_relations(self) -> None:
        def _map_pipe_connected_asset_relations(pipe_data, assets_data):
            node_id = f"{pipe_data['asset_id']}-{pipe_data['gisid']}"

            if not self.G.has_node(node_id):
                self.G.add_node(
                    node_id,
                    coords=pipe_data["geometry"].coords[0][0],
                    **pipe_data,
                )

            self._set_connected_asset_relations(pipe_data, assets_data)

        list(
            map(
                _map_pipe_connected_asset_relations,
                self.all_pipe_data,
                self.all_asset_positions,
            )
        )

        # pos = nx.get_node_attributes(self.G, "coords")
        # # https://stackoverflow.com/questions/28372127/add-edge-weights-to-plot-output-in-networkx
        # nx.draw(
        #     self.G,
        #     pos=pos,
        #     node_size=10,
        #     linewidths=1,
        #     font_size=15,
        # )
        # plt.show()

    def _create_networkx_graph(self) -> None:
        self._set_pipe_connected_asset_relations()
        # use when setting up multiprocessing
        # https://stackoverflow.com/questions/32652149/combine-join-networkx-graphs
