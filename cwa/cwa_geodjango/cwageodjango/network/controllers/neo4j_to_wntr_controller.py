import pdb

import numpy as np
from neomodel import db
import wntr
from cleanwater.transform import Neo4j2Wntr  # Adjust import path as needed
from cwageodjango.config.settings import sqids  # Adjust import path as needed

class Convert2Wntr(Neo4j2Wntr):
    """
    Class for converting Neo4j graph data to Water Network Toolkit (WNTR) format.

    Inherits from Neo4j2Wntr class.

    Parameters:
        config: Configuration object containing settings for the conversion.

    Attributes:
        config: Configuration object containing settings for the conversion.
        valve_types: List of valve types to choose from.
    """

    def __init__(self, config):
        self.config = config
        self.valve_types = ['PRV', 'PSV', 'FCV', 'TCV']  # Example valve types
        super().__init__(sqids)

    def query_graph(self, batch_size, query_limit):
        """
        Generator function to query the graph database in batches.

        Parameters:
            batch_size (int): Size of each batch for querying the graph database.
            query_limit (int): Total limit for querying the graph database.

        Yields:
            results: Result object containing batched query results.
        """
        offset = 0
        total_loaded = 0
        batches_processed = 0

        while total_loaded < query_limit:
            results, meta = db.cypher_query(
                f"""
                MATCH (n)-[r]-(m)
                WHERE NOT (r:IN_UTILITY OR r:IN_DMA) 
                RETURN n, r, m
                SKIP {offset}
                LIMIT {batch_size}
                """
            )
            records = list(results)
            total_loaded += len(records)
            batches_processed += 1

            if not records:
                break

            yield results
            offset += batch_size

            if len(records) < batch_size:
                break

    def convert(self):
        """
        Converts the Neo4j graph data to WNTR format.
        """
        # Query graph once and process nodes and edges
        graph_data = self.query_graph(self.config.batch_size, self.config.query_limit)
        for sub_graph in graph_data:
            print("processing nodes")
            self.create_nodes_and_assets(sub_graph)
            print("processing edges")
            self.create_links_and_assets(sub_graph)

    def create_nodes_and_assets(self, graph):
        """
        Create nodes and their associated assets (e.g., reservoirs) from Neo4j graph data.

        Parameters:
            graph (list): List of results from Neo4j query.
        """
        unique_node_ids = set()  # Set to store unique node IDs

        for attributes in graph:
            start = attributes[1]._start_node
            start_id = start._id

            if start_id not in unique_node_ids:
                coordinates = self.convert_coords(start['coords_27700'])

                # Check if node has asset
                asset = db.cypher_query(f"MATCH (n)-[r:HAS_ASSET]->(a) WHERE id(n)={start_id} RETURN a")[0]
                if asset:
                    asset_node = asset[0][0]
                    if "OperationalSite" in asset_node.labels:
                        base_head = 20.0  # Example base head
                        res_id = self.generate_unique_id(start_id)
                        self.wn.add_reservoir(res_id, base_head=base_head, coordinates=coordinates)
                    elif "NetworkOptValve" in asset_node.labels:
                        continue
                    else:
                        self.add_node(start_id, coordinates)
                else:
                    # No asset, add as junction
                    self.add_node(start_id, coordinates)

                unique_node_ids.add(start_id)  # Add node ID to set of processed nodes

            end = attributes[1]._end_node
            end_id = end._id

            if end_id not in unique_node_ids:
                coordinates = self.convert_coords(end['coords_27700'])

                # Check if node has asset
                asset = db.cypher_query(f"MATCH (n)-[r:HAS_ASSET]->(a) WHERE id(n)={end_id} RETURN a")[0]
                if asset:
                    asset_node = asset[0][0]
                    if "OperationalSite" in asset_node.labels:
                        base_head = 20.0  # Example base head
                        res_id = self.generate_unique_id(end_id)
                        self.wn.add_reservoir(res_id, base_head=base_head, coordinates=coordinates)
                    elif "NetworkOptValve" in asset_node.labels:
                        continue
                    else:
                        self.add_node(end_id, coordinates)
                else:
                    # No asset, add as junction
                    self.add_node(end_id, coordinates)

                unique_node_ids.add(end_id)  # Add node ID to set of processed nodes

    def create_links_and_assets(self, graph):
        """
        Create links (pipes and valves) and their associated assets (e.g., valves) from Neo4j graph data.

        Parameters:
            graph (list): List of results from Neo4j query.
        """
        for attributes in graph:
            start = attributes[1]._start_node
            start_node_id = self.generate_unique_id(start._id)

            end = attributes[1]._end_node
            end_node_id = self.generate_unique_id(end._id)

            edge_id = attributes[1]._id
            diameter = attributes[1].get('diameter', 0.1)  # Default diameter
            length = attributes[1].get('segment_length', 1.0)  # Default length
            roughness = self.roughness_values.get(attributes[1].get('material'), 120)

            # Handle link assets
            self.add_link_assets(start, start_node_id, end, end_node_id, diameter)

            if not self.is_asset(start) and not self.is_asset(end):
                self.add_pipe(edge_id, start_node_id, end_node_id, diameter, length, roughness)

    def add_link_assets(self, start_node, start_node_id, end_node, end_node_id, diameter):
        """
        Add link assets (e.g., valves) to the WNTR model.

        Parameters:
            start_node (neomodel Node): Start node of the link.
            start_node_id (str): WNTR start node ID.
            end_node (neomodel Node): End node of the link.
            end_node_id (str): WNTR end node ID.
            diameter (float): Diameter of the link.
        """
        if "NetworkOptValve" in start_node.labels or "PressureControlValve" in start_node.labels:
            connected_nodes, diameter = self.get_connected_nodes(start_node)
            valve_type = np.random.choice(self.valve_types)
            if len(connected_nodes) == 2:
                self.wn.add_valve(start_node_id, connected_nodes[0], connected_nodes[1], diameter, valve_type)
        elif "NetworkOptValve" in end_node.labels or "PressureControlValve" in end_node.labels:
            connected_nodes, diameter = self.get_connected_nodes(end_node)
            valve_type = np.random.choice(self.valve_types)
            if len(connected_nodes) == 2:
                self.wn.add_valve(end_node_id, connected_nodes[0], connected_nodes[1], diameter, valve_type)

    def is_asset(self, node):
        """
        Check if a node is an asset.

        Parameters:
            node (neomodel Node): Node to check.

        Returns:
            bool: True if the node is an asset, False otherwise.
        """
        asset = db.cypher_query(f"MATCH (n)-[r:HAS_ASSET]->(a) WHERE id(n)={node._id} RETURN a")[0]
        return bool(asset)

    def get_connected_nodes(self, node):
        """
        Get the IDs of nodes connected to the given node, excluding any nodes that are assets.

        Parameters:
            node (neomodel Node): Node to find connected nodes for.

        Returns:
            connected_node_ids (list): List of connected node IDs.
            diameter (float): Diameter of the pipe connecting the nodes.
        """
        results, _ = db.cypher_query(f"MATCH (n)-[r:PipeMain]-(m) WHERE id(n)={node._id} RETURN r, m")

        connected_nodes = []
        coords = []
        ids = []
        diameter = None

        for result in results:
            relationship = result[0]
            connected_node = result[1]

            if 'Asset' not in connected_node.labels:
                ids.append(connected_node.id)
                connected_nodes.append(self.generate_unique_id(connected_node.id))
                coords.append(connected_node['coords_27700'])

            if diameter is None:  # Assuming all connections have the same diameter
                diameter = relationship['diameter']

        self.add_node(ids[1], coords[1])
        return connected_nodes, diameter

    def wntr_to_inp(self):
        """
        Write the WNTR model to EPANET INP file format.

        Parameters:
            filename (str): Name of the output file.
        """
        wntr.network.write_inpfile(self.wn, filename=self.config.outputfile)

    def wntr_to_json(self):
        """
        Write the WNTR model to JSON file format.

        Parameters:
            filename (str): Name of the output file.
        """
        wntr.utils.network.write_json(self.wn, filename=self.config.outputfile)
