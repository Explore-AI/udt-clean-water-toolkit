import pdb

import numpy as np
import wntr
from wntr.network import Pipe, Valve
from neomodel import db
from cleanwater.transform import Neo4j2Wntr
from cwageodjango.config.settings import sqids


class Convert2Wntr(Neo4j2Wntr):
    """
    Class for converting Neo4j graph data to Water Network Toolkit (WNTR) format.

    Inherits from Neo4j2Wntr class.

    Parameters:
        config: Configuration object containing settings for the conversion.

    Attributes:
        config: Configuration object containing settings for the conversion.
        valve_types: List of valve types to choose from.
        wn: WNTR WaterNetworkModel instance.
        node_to_edges: Dictionary mapping nodes to their outgoing edges.
        nx_graph: NetworkX directed graph representation of the network.
    """

    def __init__(self, config):
        super().__init__(sqids)
        self.config = config
        self.all_nodes = set()
        self.all_edges = set()  # List to store all edges
        self.node_to_edges = {}  # Dictionary for mapping nodes to their outgoing edges
        self.valve_types = ['PRV', 'PSV', 'FCV', 'TCV']  # Example valve types
        self.wn = wntr.network.WaterNetworkModel()  # Initialize WNTR model

    @staticmethod
    def query_graph(batch_size, query_limit):
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

        while total_loaded < query_limit:
            try:
                results, meta = db.cypher_query(
                    f"""
                    MATCH (n)-[r]-(m)
                    WHERE NOT (r:IN_UTILITY OR r:IN_DMA) 
                    RETURN n, r, m
                    SKIP {offset}
                    LIMIT {batch_size}
                    """
                )
            except Exception as e:
                print(f"Error querying the database: {e}")
                break

            records = list(results)
            total_loaded += len(records)
            offset += batch_size

            if not records:
                break

            yield results

    def convert(self):
        """
        Converts the Neo4j graph data to WNTR format.
        """

        print("Compiling nodes and edges")
        graph_data = self.query_graph(self.config.batch_size, self.config.query_limit)
        for sub_graph in graph_data:
            for record in sub_graph:
                start_node = record[0]
                relation = record[1]
                end_node = record[2]

                # Add start and end nodes to set of all nodes
                self.all_nodes.add(start_node)
                self.all_nodes.add(end_node)

                # Add edge to list of all edges
                self.all_edges.add(relation)

                # Map nodes to their outgoing edges
                if start_node not in self.node_to_edges:
                    self.node_to_edges[start_node] = []
                self.node_to_edges[start_node].append((start_node, relation, end_node))

        print("Processing nodes")
        for node in self.all_nodes:
            if self.is_valve(node._id):
                self.handle_valve_nodes(node)
            if not self.is_valve(node._id):
                self.create_nodes_and_assets(node)

        print("Processing edges")
        for node in self.all_nodes:
            if self.is_valve(node._id):
                self.create_valve_edges(node)

        self.create_links_and_assets()

    def handle_valve_nodes(self, valve_node):
        valve_id = valve_node._id
        coordinates = self.convert_coords(valve_node['coords_27700'])
        new_start_node_id = self.generate_unique_id(valve_id) + "_valve_start"
        new_end_node_id = self.generate_unique_id(valve_id) + "_valve_end"
        self.add_node(self.generate_unique_id(valve_id), coordinates)
        self.add_node(new_start_node_id, coordinates)  # Replace 'coordinates' with appropriate value
        self.add_node(new_end_node_id, coordinates)  # Replace 'coordinates' with appropriate value

    def create_nodes_and_assets(self, node):
        """
        Create nodes and their associated assets (e.g., reservoirs) from Neo4j graph data.

        Parameters:
            node: specific node from graph query.
        """

        coordinates = self.convert_coords(node['coords_27700'])

        # Check if node has asset
        if self.is_reservoir(node._id):
            base_head = 20.0  # Example base head
            res_id = self.generate_unique_id(node._id)
            self.wn.add_reservoir(res_id, base_head=base_head, coordinates=coordinates)
        else:
            # No asset, add as junction
            node_id = self.generate_unique_id(node._id)
            self.add_node(node_id, coordinates)

    def create_valve_edges(self, valve_node):
        """
        Process a valve node by replacing it with a triad (node, edge, node).

        Parameters:
            valve_node: Valve node from Neo4j graph data.
        """
        valve_id = valve_node._id
        valve_type = np.random.choice(self.valve_types)  # Choose valve type
        outgoing_edges = self.node_to_edges.get(valve_node, [])
        if len(outgoing_edges) == 1:
            end_node_id = self.generate_unique_id(outgoing_edges[0][2]._id)
            relation = outgoing_edges[0][1]
            new_start_node_id = self.generate_unique_id(valve_id) + "_valve_start"
            new_end_node_id = self.generate_unique_id(valve_id) + "_valve_end"
            valve_link_id = self.generate_unique_id(valve_id) + "_" + valve_type + "_valve"
            diameter = relation["diameter"]
            length = relation["segment_length"]
            roughness = self.roughness_values.get(relation["material"].lower())

            # Create edge connecting the new nodes
            valve = Valve(valve_link_id,
                          new_start_node_id,
                          new_end_node_id,
                          self.wn)

            self.wn.add_valve(valve_link_id,
                              new_start_node_id,
                              new_end_node_id,
                              diameter,
                              valve_type,
                              initial_status='OPEN')
            # Update existing edge to connect to the new nodes
            self.add_pipe(relation._id, end_node_id, new_start_node_id, diameter, length, roughness)

        else:
            start_node1 = outgoing_edges[0][2]
            relation1 = outgoing_edges[0][1]
            relation2 = outgoing_edges[1][1]
            end_node2 = outgoing_edges[1][2]

            start_node1_id = self.generate_unique_id(start_node1._id)
            length1 = relation1["segment_length"]
            diameter1 = relation1["diameter"]
            roughness1 = self.roughness_values.get(relation1["material"].lower())

            end_node2_id = self.generate_unique_id(end_node2._id)
            length2 = relation2["segment_length"]
            diameter2 = relation2["diameter"]
            roughness2 = self.roughness_values.get(relation2["material"].lower())

            new_start_node_id = self.generate_unique_id(valve_id) + "_valve_start"
            new_end_node_id = self.generate_unique_id(valve_id) + "_valve_end"
            valve_link_id = self.generate_unique_id(valve_id) + "_" + valve_type + "_valve"

            # Create edge connecting the new nodes
            valve = Valve(valve_link_id,
                          new_start_node_id,
                          new_end_node_id,
                          self.wn)

            self.wn.add_valve(valve_link_id,
                              new_start_node_id,
                              new_end_node_id,
                              diameter1,
                              valve_type,
                              initial_status='OPEN')
            # pdb.set_trace()
            # Update existing edge to connect to the new nodes
            self.add_pipe(relation1._id, start_node1_id, new_start_node_id, diameter1, length1, roughness1)
            self.add_pipe(relation2._id, new_end_node_id, end_node2_id, diameter2, length2, roughness2)

    def create_links_and_assets(self):
        """
        Create links (pipes) and their associated assets (e.g., valves) from Neo4j graph data.
        """
        for edge in self.all_edges:
            start_node = edge._start_node
            end_node = edge._end_node

            start_node_id = self.generate_unique_id(start_node._id)
            end_node_id = self.generate_unique_id(end_node._id)
            diameter = edge["diameter"]
            length = edge["segment_length"]
            roughness = self.roughness_values.get(edge['material'].lower())

            if self.is_valve(start_node._id) or self.is_valve(end_node._id):
                # Skip valve edges (already processed in create_valve_edges)
                continue

            self.add_pipe(edge._id, start_node_id, end_node_id, diameter, length, roughness)

    def wntr_to_inp(self):
        """
        Write the WNTR model to EPANET INP file format.
        """
        wntr.network.write_inpfile(self.wn, filename=self.config.outputfile)

    @staticmethod
    def is_reservoir(node_id):
        """
        Check if a node represents a reservoir.

        Parameters:
            node_id: ID of the node.

        Returns:
            bool: True if the node represents a reservoir, False otherwise.
        """
        asset_query = f"""
                MATCH (n)-[r:HAS_ASSET]->(a:OperationalSite) 
                WHERE id(n)={node_id} 
                RETURN a
                """
        reservoir = db.cypher_query(asset_query)[0]
        return bool(reservoir)

    @staticmethod
    def is_valve(node_id):
        """
        Check if a node represents a valve.

        Parameters:
            node_id: ID of the node.

        Returns:
            bool: True if the node represents a valve, False otherwise.
        """
        asset_query = f"""
                MATCH (n)-[r:HAS_ASSET]->(a) 
                WHERE id(n)={node_id} AND (a:NetworkOptValve OR a:PressureControlValve)
                RETURN a
                """
        valve = db.cypher_query(asset_query)[0]
        return bool(valve)
