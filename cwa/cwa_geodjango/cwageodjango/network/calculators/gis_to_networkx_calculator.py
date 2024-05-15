import pdb
import json
from networkx import Graph
import networkx as nx
from cleanwater.calculators import GisToGraphCalculator
from cwageodjango.config.settings import sqids
from neomodel import db
#from neo4j.types.graph import Node, Relationship
import matplotlib.pyplot as plt
import contextily as ctx
import geopandas as gpd
from shapely import wkt
from shapely.geometry import Point
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

class GisToNxCalculator(GisToGraphCalculator):
    """Create a NetworkX graph of assets from a geospatial
    network of assets"""

    def __init__(self, config):
        self.config = config
        self.G: Graph = Graph()

        self.all_edges_by_pipe = []
        self.all_nodes_by_pipe = []

        super().__init__(
            self.config.srid,
            sqids,
            processor_count=config.processor_count,
            chunk_size=config.chunk_size,
            neoj4_point=self.config.neoj4_point,
        )

    def create_nx_graph(self) -> None:
        """Iterate over pipes and connect related pipe interactions
        and point assets. Uses a map method to operate on the pipe
        and asset data.

        Params:
              None
        Returns:
              None
        """
        # edges = self._gather_edges()
        # nodes = self._gather_nodes()
        # self.G = nx.Graph()
        # self._add_nodes_to_graph(nodes)
        # self._add_edges_to_graph(edges)
        # self._remove_unconnected_nodes()
        # self._connected_components()
        # G = self.G
        # dma_codes = GisToNxCalculator.get_dma_codes_from_graph(G)
        # self.plot_graph(G, dma_codes, 'networkx')
        # self.spatial_plot(G, dma_codes, 'networkx')
        # nx.write_graphml(self.G, "networkx_graph.graphml")

        dma_codes = self.config.dma_codes
        #pdb.set_trace()
        for dma_code in dma_codes:
            query = f"""
            MATCH (n)-[r]-(m)
            WHERE n.dmas contains '{dma_code}'
            RETURN n, r, m
            """
            all_nodes = []
            all_relationships = []
            results = db.cypher_query(query)

            for records in results:
                for data in records:
                    # Initialize variables for node and relationship data
                    node_n = None
                    node_m = None
                    relationship_r = None

                    # Extract node and relationship data from the record
                    try:
                        node_n = data[0]
                        all_nodes.append(node_n)
                    except IndexError:
                        print("Index out of range error occurred while extracting nodes.")
                    try:
                        node_m = data[2]
                        all_nodes.append(node_m)
                    except IndexError:
                        print("Index out of range error occurred while extracting nodes.")
                    try:
                        relationship_r = data[1]
                        all_relationships.append(relationship_r)
                    except IndexError:
                        print("Index out of range error occurred while extracting relationship.")

            # Remove duplicates from the lists
            #pdb.set_trace()
            all_nodes = list(set(all_nodes))
            all_relationships = list(set(all_relationships))
            #pdb.set_trace()
            nxgraph = nx.Graph()
            for node in all_nodes:
                if isinstance(node, str):
                    print("Node is a string:", node)
                #pdb.set_trace()
                else:
                    nxgraph.add_node(node['node_key'],
                                     coords_27700=node['coords_27700'],
                                     node_labels=GisToNxCalculator.node_label(node),
                                     dmas=node['dmas'])
            #pdb.set_trace()
            for edge in all_relationships:
                if isinstance(edge, str):
                    print("Node is a string:", edge)
                else:
                    dmas = edge.nodes[1]['dmas'] if edge.nodes[1]['dmas'] is not None \
                        else edge.nodes[0]['dmas']
                    nxgraph.add_edge(edge.nodes[0]['node_key'],
                                     edge.nodes[1]['node_key'],
                                     gid=edge['gid'],
                                     segment_wkt=edge['segment_wkt'],
                                     asset_label=edge.type,
                                     dmas=dmas)
            #pdb.set_trace()
            self.plot_graph(nxgraph, [dma_code], 'neo4j')
            self.spatial_plot(nxgraph, [dma_code], 'neo4j')

    @staticmethod
    def node_label(node):
        label = None
        labels = list(node.labels)
        if 'PipeEnd' in labels:
            label = ['PipeEnd']
        elif 'Hydrant' in labels:
            label = ['Hydrant']
        elif 'NetworkOptValve' in labels:
            label = ['NetworkOptValve']
        else:
            label = ['pipe_junction']
        return label

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
        print('Connected components:', connected)

    @staticmethod
    def plot_graph(G, dma_codes, source):
        from datetime import datetime
        # Get the current date and time
        now = datetime.now()
        # Format the datetime object as a string
        formatted_date_time = now.strftime("%Y%m%d%H%M")
        if dma_codes:
            for dma in dma_codes:
                filename = f"dma_{dma}_graph_from_{source}_{formatted_date_time}.svg"

                # Define edge positions
                pos = nx.spring_layout(G, scale=10)

                # Extracting node and edge labels from the graph
                node_labels = nx.get_node_attributes(G, "node_labels").values()
                edge_labels = nx.get_edge_attributes(G, "asset_name").values()
                #pdb.set_trace()
                # Define colour map based on node and edge labels
                nodes_colour_map = ['red' if 'PipeEnd' in labels
                                    else 'blue' if 'Hydrant' in labels
                                    else 'yellow' if 'NetworkOptValve' in labels
                                    else 'green' if 'Pipe_Junction'
                                    else 'green' for labels in node_labels]

                edges_colour_map = ['black' if 'TrunkMain' in labels
                                    else 'orange' for labels in edge_labels]

                # Draw the graph nodes and edges
                plt.figure(figsize=(30, 30))
                nx.draw(
                    G, pos, with_labels=False, node_color=nodes_colour_map, node_size=15, font_size=2
                )
                nx.draw_networkx_edges(G, pos, edge_color=edges_colour_map, width=1)

                # Draw edge labels using the gid attribute
                #edge_labels = nx.get_edge_attributes(G, "gid")
                #nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
                plt.savefig(filename, format="svg")
                plt.close()
                print(f"file {filename} successfully saved")
        else:
            filename = f"dma_unknown_graph_from_{source}_{formatted_date_time}.svg"

            # Define edge positions
            pos = nx.spring_layout(G, scale=10)

            # Extracting node and edge labels from the graph
            node_labels = nx.get_node_attributes(G, "node_labels").values()
            edge_labels = nx.get_edge_attributes(G, "asset_name").values()

            # Define colour map based on node and edge labels
            nodes_colour_map = ['red' if 'PipeEnd' in labels
                                else 'blue' if 'Hydrant' in labels
                                else 'yellow' if 'NetworkOptValve' in labels
                                else 'green' for labels in node_labels]

            edges_colour_map = ['black' if 'TrunkMain' in labels
                                else 'orange' for labels in edge_labels]
            #pdb.set_trace()
            # Draw the graph nodes and edges
            plt.figure(figsize=(30, 30))
            nx.draw(
                G, pos, with_labels=False, node_color=nodes_colour_map, node_size=15, font_size=2
            )
            nx.draw_networkx_edges(G, pos, edge_color=edges_colour_map, width=1)

            # Draw edge labels using the gid attribute
            edge_labels = nx.get_edge_attributes(G, "gid")
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
            plt.savefig(filename, format="svg")
            plt.close()
            print(f"file {filename} successfully saved")

    @staticmethod
    def spatial_plot(G, dma_codes, source):
        from datetime import datetime
        # Get the current date and time
        now = datetime.now()
        # Format the datetime object as a string
        formatted_date_time = now.strftime("%Y%m%d%H%M")
        icon_path = 'icons8-hydrant-60.png'
        if dma_codes:
            for dma in dma_codes:
                filename = f'dma_{dma}_SpatialPlot_from_{source}_{formatted_date_time}.svg'
                # if no dma codes, plot entire graph, otherwise filter by code, produce one map per code
                nodes_gdf = GisToNxCalculator._create_nodes_gdf(G)
                edges_gdf = GisToNxCalculator._create_edges_gdf(G)
                #pdb.set_trace()
                # Define colour mapping dictionaries
                default_node_colour = 'gray'
                default_edge_colour = 'gray'
                nodes_colour_map = {'Hydrant': 'blue', 'NetworkOptValve': 'yellow', 'pipe_junction': 'red'}
                edges_colour_map = {'TrunkMain': 'black', 'DistributionMain': 'orange'}

                nodes_gdf['node_colour'] = nodes_gdf['node_label'].map(lambda x: nodes_colour_map.get(x, default_node_colour))
                edges_gdf['edge_colour'] = edges_gdf['asset_label'].map(lambda x: edges_colour_map.get(x, default_edge_colour))

                # Plot GeoDataFrames
                fig, ax = plt.subplots(figsize=(30, 30))
                edges_gdf.plot(ax=ax,
                               color=edges_gdf['edge_colour'],
                               label='Pipe Features',
                               legend=True,
                               zorder=1)
                nodes_gdf.plot(ax=ax,
                               color=nodes_gdf['node_colour'],
                               markersize=5,
                               label='Point Assets',
                               legend=True,
                               zorder=2)

                # Add OpenStreetMap basemap
                ctx.add_basemap(ax, crs=edges_gdf.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)

                def add_icon(x, y, ax):
                    img = plt.imread(icon_path)
                    imagebox = OffsetImage(img, zoom=0.2)
                    ab = AnnotationBbox(imagebox, (x, y), frameon=False, pad=0)
                    ax.add_artist(ab)

                hydrants_gdf = nodes_gdf[nodes_gdf['node_label'] == "Hydrant"]

                # Plot the points and add the raster image as an icon
                for x, y in zip(hydrants_gdf.geometry.x, hydrants_gdf.geometry.y):
                    ax.plot(x, y, marker='None')
                    add_icon(x, y, ax)

                # Add labels for nodes and edges
                # for idx, row in nodes_gdf.iterrows():
                #     ax.annotate(text=row['node_key'], xy=(row['geometry'].x, row['geometry'].y), xytext=(3, 3),
                #                 textcoords="offset points")

                # for idx, row in edges_gdf.iterrows():
                #     ax.annotate(text=row['gid'], xy=(row['geometry'].coords[0]), xytext=(3, 3),
                #                 textcoords="offset points")

                # Add legend, title
                ax.legend()
                ax.set_title('Neo4j Graph as Geo-Spatial Plot')

                # Save plot as SVG
                plt.savefig(filename, format='svg')
                plt.close()
                print(f"file {filename} successfully saved")
        else:
            filename = f'dma_unknown_SpatialPlot_from_{source}_{formatted_date_time}.svg'
            # if no dma codes, plot entire graph, otherwise filter by code, produce one map per code
            nodes_gdf = GisToNxCalculator._create_nodes_gdf(G)
            edges_gdf = GisToNxCalculator._create_edges_gdf(G)

            # Define colour mapping dictionaries
            default_node_colour = 'gray'
            default_edge_colour = 'gray'
            nodes_colour_map = {'Hydrant': 'blue', 'NetworkOptValve': 'yellow', 'pipe_junction': 'red'}
            edges_colour_map = {'TrunkMain': 'black', 'DistributionMain': 'orange'}

            nodes_gdf['node_colour'] = nodes_gdf['node_label'].map(
                lambda x: nodes_colour_map.get(x, default_node_colour))
            edges_gdf['edge_colour'] = edges_gdf['asset_label'].map(
                lambda x: edges_colour_map.get(x, default_edge_colour))

            # Plot GeoDataFrames
            fig, ax = plt.subplots(figsize=(30, 30))
            edges_gdf.plot(ax=ax, color=edges_gdf['edge_colour'], label='Pipe Features', legend=True)
            nodes_gdf.plot(ax=ax, color=nodes_gdf['node_colour'], markersize=5, label='Point Assets', legend=True)

            # Add OpenStreetMap basemap
            ctx.add_basemap(ax, crs=edges_gdf.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)

            # Add labels for nodes and edges
            # for idx, row in nodes_gdf.iterrows():
            #     ax.annotate(text=row['node_key'], xy=(row['geometry'].x, row['geometry'].y), xytext=(3, 3),
            #                 textcoords="offset points")

            # for idx, row in edges_gdf.iterrows():
            #     ax.annotate(text=row['gid'], xy=(row['geometry'].coords[0]), xytext=(3, 3),
            #                 textcoords="offset points")

            # Add legend, title
            ax.legend()
            ax.set_title('Neo4j Graph as Geo-Spatial Plot')

            # Save plot as SVG
            plt.savefig(filename, format='svg')
            plt.close()
            print(f"file {filename} successfully saved")

    @staticmethod
    def _create_nodes_gdf(nxgraph):
        # Extract attributes for each node
        node_data = []
        for node, attributes in nxgraph.nodes(data=True):
            node_key = node
            node_label = attributes.get('node_labels')[-1]
            dmas_str = attributes.get('dmas', '[]')
            dmas = json.loads(dmas_str)
            dma_code = dmas[0]['code']
            coords = attributes.get('coords_27700')
            x_coord, y_coord = coords
            geometry = Point(x_coord, y_coord)
            node_data.append((node_key, node_label, dma_code, geometry))

        # Create GeoDataFrame for nodes
        nodes_gdf = gpd.GeoDataFrame(node_data,
                                     columns=['node_key', 'node_label', 'dma_code', 'geometry'],
                                     crs='EPSG:27700')

        # pdb.set_trace()
        return nodes_gdf

    @staticmethod
    def _create_edges_gdf(nxgraph):
        # Extracting attributes for each edge
        edge_data = []
        for source, target, attributes in nxgraph.edges(data=True):
            gid = attributes.get('gid')
            asset_label = attributes.get('asset_label')
            dmas_str = attributes.get('dmas', '[]')
            dmas = json.loads(dmas_str)
            dma_code = dmas[0]['code']
            segment_wkt = attributes.get('segment_wkt')
            geometry = wkt.loads(segment_wkt)
            edge_data.append((gid, asset_label, dma_code, geometry))

        # Create GeoDataFrame for edges
        edges_gdf = gpd.GeoDataFrame(edge_data,
                                     columns=['gid', 'asset_label', 'dma_code', 'geometry'],
                                     crs='EPSG:27700')

        return edges_gdf

    @staticmethod
    def get_dma_codes_from_graph(nxgraph):
        # method for collecting list of DMA codes from graph
        dma_codes = []
        for _, attributes in nxgraph.nodes(data=True):
            dmas_str = attributes.get('dmas', '[]')
            dmas = json.loads(dmas_str)
            dma_code = dmas[0]['code']
            if dma_code not in dma_codes:
                dma_codes.append(dma_code)

        return dma_codes
