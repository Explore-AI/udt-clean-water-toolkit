import json
from networkx import Graph
import networkx as nx
from cleanwater.transform import GisToGraph
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely import wkt
from shapely.geometry import Point

class GisToNx(GisToGraph):
    """Create a NetworkX graph of assets from a geospatial
    network of assets"""

    def __init__(self, srid, sqids, point_asset_names: list = []):
        self.srid = srid
        self.sqids = sqids
        self.G: Graph = Graph()

        self.all_edges_by_pipe = []
        self.all_nodes_by_pipe = []

        super().__init__(srid, sqids, point_asset_names=point_asset_names)

    def create_nx_graph(self) -> None:
        """Iterate over pipes and connect related pipe interactions
        and point assets. Uses a map method to operate on the pipe
        and asset data.

        Params:
              None
        Returns:
              None
        """

        print("yellow")
        import pdb

        pdb.set_trace()
        edges = self._gather_edges()
        nodes = self._gather_nodes()
        self.G = nx.Graph()
        self._add_nodes_to_graph(nodes)
        self._add_edges_to_graph(edges)
        self._remove_unconnected_nodes()
        self._connected_components()
        self._plot_graph()
        self._spatial_plot()

    def _gather_edges(self):
        edges = []
        for sublist in self.all_edges_by_pipe:
            for edge in sublist:
                edges.append(edge)

        return edges

    def _gather_nodes(self):
        nodes = []
        for sublist in self.all_nodes_by_pipe:
            for node in sublist:
                nodes.append(node)

        return nodes

    def _add_nodes_to_graph(self, nodes):
        unique_nodes = []
        unique_node_keys = []
        for node in nodes:
            if node["node_key"] not in unique_node_keys:
                unique_nodes.append(node)
                unique_node_keys.append(node["node_key"])

        for node in unique_nodes:
            node_id = node["node_key"]
            attributes = {
                key: value for key, value in node.items() if key != "node_key"
            }
            self.G.add_node(node_id, **attributes)

    def _add_edges_to_graph(self, edges):
        # Add edges to the graph with attributes
        for edge in edges:
            from_node = edge["from_node_key"]
            to_node = edge["to_node_key"]
            attributes = {
                key: value
                for key, value in edge.items()
                if key not in ["from_node_key", "to_node_key"]
            }
            self.G.add_edge(from_node, to_node, **attributes)

    def _remove_unconnected_nodes(self):
        # Get a list of isolated nodes
        isolated_nodes = list(nx.isolates(self.G))

        # Remove isolated nodes from the graph
        self.G.remove_nodes_from(isolated_nodes)
        num_isolated_nodes = len(isolated_nodes)
        print("Number of isolated nodes removed:", num_isolated_nodes)

    def _connected_components(self):
        connected = len(list(nx.connected_components(self.G)))
        print("Connected components:", connected)

    def _plot_graph(self):
        dma_codes = self._get_dma_codes_from_graph(self.G)
        if dma_codes:
            for dma in dma_codes:
                filename = f"dma_{dma}_graph.svg"

                # Define edge positions
                pos = nx.spring_layout(self.G, scale=10)

                # Extracting node and edge labels from the graph
                node_labels = nx.get_node_attributes(self.G, "node_labels").values()
                edge_labels = nx.get_edge_attributes(self.G, "asset_name").values()

                # Define colour map based on node and edge labels
                nodes_colour_map = [
                    (
                        "blue"
                        if "Hydrant" in labels
                        else "yellow" if "NetworkOptValve" in labels else "red"
                    )
                    for labels in node_labels
                ]

                edges_colour_map = [
                    "black" if "TrunkMain" in labels else "orange"
                    for labels in edge_labels
                ]

                # Draw the graph nodes and edges
                plt.figure(figsize=(30, 30))
                nx.draw(
                    self.G,
                    pos,
                    with_labels=False,
                    node_color=nodes_colour_map,
                    node_size=15,
                    font_size=2,
                )
                nx.draw_networkx_edges(self.G, pos, edge_color=edges_colour_map, width=1)

                # Draw edge labels using the gid attribute
                edge_labels = nx.get_edge_attributes(self.G, "gid")
                nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
                plt.savefig(filename, format="svg")
                plt.close()
                print(f"file {filename} successfully saved")
        else:
            filename = "dma_unknown_graph.svg"

            # Define edge positions
            pos = nx.spring_layout(self.G, scale=10)

            # Extracting node and edge labels from the graph
            node_labels = nx.get_node_attributes(self.G, "node_labels").values()
            edge_labels = nx.get_edge_attributes(self.G, "asset_name").values()

            # Define colour map based on node and edge labels
            nodes_colour_map = [
                (
                    "blue"
                    if "Hydrant" in labels
                    else "yellow" if "NetworkOptValve" in labels else "red"
                )
                for labels in node_labels
            ]

            edges_colour_map = [
                "black" if "TrunkMain" in labels else "orange" for labels in edge_labels
            ]

            # Draw the graph nodes and edges
            plt.figure(figsize=(30, 30))
            nx.draw(
                self.G,
                pos,
                with_labels=False,
                node_color=nodes_colour_map,
                node_size=15,
                font_size=2,
            )
            nx.draw_networkx_edges(self.G, pos, edge_color=edges_colour_map, width=1)

            # Draw edge labels using the gid attribute
            edge_labels = nx.get_edge_attributes(self.G, "gid")
            nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
            plt.savefig(filename, format="svg")
            plt.close()
            print(f"file {filename} successfully saved")

    def _spatial_plot(self):
        dma_codes = self._get_dma_codes_from_graph(self.G)
        if dma_codes:
            for dma in dma_codes:
                filename = f"dma_{dma}_SpatialPlot.svg"
                # if no dma codes, plot entire graph, otherwise filter by code, produce one map per code
                nodes_gdf = self._create_nodes_gdf(self.G)
                edges_gdf = self._create_edges_gdf(self.G)

                # Define colour mapping dictionaries
                default_node_colour = "gray"
                default_edge_colour = "gray"
                nodes_colour_map = {
                    "Hydrant": "blue",
                    "NetworkOptValve": "yellow",
                    "pipe_junction": "red",
                }
                edges_colour_map = {"TrunkMain": "black", "DistributionMain": "orange"}

                nodes_gdf["node_colour"] = nodes_gdf["node_label"].map(
                    lambda x: nodes_colour_map.get(x, default_node_colour)
                )
                edges_gdf["edge_colour"] = edges_gdf["asset_label"].map(
                    lambda x: edges_colour_map.get(x, default_edge_colour)
                )

                # Plot GeoDataFrames
                fig, ax = plt.subplots(figsize=(30, 30))
                edges_gdf.plot(
                    ax=ax,
                    color=edges_gdf["edge_colour"],
                    label="Pipe Features",
                    legend=True,
                )
                nodes_gdf.plot(
                    ax=ax,
                    color=nodes_gdf["node_colour"],
                    markersize=5,
                    label="Point Assets",
                    legend=True,
                )

                # Add OpenStreetMap basemap
                # ctx.add_basemap(ax, crs=edges_gdf.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)

                # Add labels for nodes and edges
                # for idx, row in nodes_gdf.iterrows():
                #     ax.annotate(text=row['node_key'], xy=(row['geometry'].x, row['geometry'].y), xytext=(3, 3),
                #                 textcoords="offset points")

                # for idx, row in edges_gdf.iterrows():
                #     ax.annotate(text=row['gid'], xy=(row['geometry'].coords[0]), xytext=(3, 3),
                #                 textcoords="offset points")

                # Add legend, title
                ax.legend()
                ax.set_title("Neo4j Graph as Geo-Spatial Plot")

                # Save plot as SVG
                plt.savefig(filename, format="svg")
                plt.close()
                print(f"file {filename} successfully saved")
        else:
            filename = "dma_unknown_SpatialPlot.svg"
            # if no dma codes, plot entire graph, otherwise filter by code, produce one map per code
            nodes_gdf = self._create_nodes_gdf(self.G)
            edges_gdf = self._create_edges_gdf(self.G)

            # Define colour mapping dictionaries
            default_node_colour = "gray"
            default_edge_colour = "gray"
            nodes_colour_map = {
                "Hydrant": "blue",
                "NetworkOptValve": "yellow",
                "pipe_junction": "red",
            }
            edges_colour_map = {"TrunkMain": "black", "DistributionMain": "orange"}

            nodes_gdf["node_colour"] = nodes_gdf["node_label"].map(
                lambda x: nodes_colour_map.get(x, default_node_colour)
            )
            edges_gdf["edge_colour"] = edges_gdf["asset_label"].map(
                lambda x: edges_colour_map.get(x, default_edge_colour)
            )

            # Plot GeoDataFrames
            fig, ax = plt.subplots(figsize=(30, 30))
            edges_gdf.plot(
                ax=ax,
                color=edges_gdf["edge_colour"],
                label="Pipe Features",
                legend=True,
            )
            nodes_gdf.plot(
                ax=ax,
                color=nodes_gdf["node_colour"],
                markersize=5,
                label="Point Assets",
                legend=True,
            )

            # Add OpenStreetMap basemap
            # ctx.add_basemap(ax, crs=edges_gdf.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)

            # Add labels for nodes and edges
            # for idx, row in nodes_gdf.iterrows():
            #     ax.annotate(text=row['node_key'], xy=(row['geometry'].x, row['geometry'].y), xytext=(3, 3),
            #                 textcoords="offset points")

            # for idx, row in edges_gdf.iterrows():
            #     ax.annotate(text=row['gid'], xy=(row['geometry'].coords[0]), xytext=(3, 3),
            #                 textcoords="offset points")

            # Add legend, title
            ax.legend()
            ax.set_title("Neo4j Graph as Geo-Spatial Plot")

            # Save plot as SVG
            plt.savefig(filename, format="svg")
            plt.close()
            print(f"file {filename} successfully saved")

    @staticmethod
    def _create_nodes_gdf(nxgraph):
        # Extract attributes for each node
        node_data = []
        for node, attributes in nxgraph.nodes(data=True):
            node_key = node
            node_label = attributes.get("node_labels")[-1]
            dmas_str = attributes.get("dmas", "[]")
            dmas = json.loads(dmas_str)
            dma_code = dmas[0]["code"]
            coords = attributes.get("coords_27700")
            x_coord, y_coord = coords
            geometry = Point(x_coord, y_coord)
            node_data.append((node_key, node_label, dma_code, geometry))

        # Create GeoDataFrame for nodes
        nodes_gdf = gpd.GeoDataFrame(
            node_data,
            columns=["node_key", "node_label", "dma_code", "geometry"],
            crs="EPSG:27700",
        )

        return nodes_gdf

    @staticmethod
    def _create_edges_gdf(nxgraph):
        # Extracting attributes for each edge
        edge_data = []
        for source, target, attributes in nxgraph.edges(data=True):
            gid = attributes.get("gid")
            asset_label = attributes.get("asset_label")
            dmas_str = attributes.get("dmas", "[]")
            dmas = json.loads(dmas_str)
            dma_code = dmas[0]["code"]
            segment_wkt = attributes.get("segment_wkt")
            geometry = wkt.loads(segment_wkt)
            edge_data.append((gid, asset_label, dma_code, geometry))

        # Create GeoDataFrame for edges
        edges_gdf = gpd.GeoDataFrame(
            edge_data,
            columns=["gid", "asset_label", "dma_code", "geometry"],
            crs="EPSG:27700",
        )

        return edges_gdf

    @staticmethod
    def _get_dma_codes_from_graph(nxgraph):
        # method for collecting list of DMA codes from graph
        dma_codes = []
        for _, attributes in nxgraph.nodes(data=True):
            dmas_str = attributes.get("dmas", "[]")
            dmas = json.loads(dmas_str)
            dma_code = dmas[0]["code"]
            if dma_code not in dma_codes:
                dma_codes.append(dma_code)

        return dma_codes
