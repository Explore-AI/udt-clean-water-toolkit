import numpy as np
from neomodel import db
from cleanwater.transform import Neo4j2Wntr
from cwageodjango.config.settings import sqids
import wntr

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
            print(f"Loaded {total_loaded} of {query_limit} results (batch size: {batch_size}, offset: {offset})")

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
        # First pass: Create nodes
        nodes_dict = {}
        for sub_graph in self.query_graph(self.config.batch_size, self.config.query_limit):
            nodes_dict.update(self.create_nodes(sub_graph))

        # Second pass: Create links (pipes and valves)
        for sub_graph in self.query_graph(self.config.batch_size, self.config.query_limit):
            self.create_links(sub_graph, nodes_dict)

    def create_nodes(self, graph):
        """
        Create nodes from Neo4j graph data.

        Parameters:
            graph (list): List of results from Neo4j query.

        Returns:
            nodes_dict (dict): Dictionary mapping node IDs to WNTR node IDs.
        """
        nodes_dict = {}
        for attributes in graph:
            start = attributes[1]._start_node
            coordinates = self.convert_coords(start['coords_27700'])
            start_id = start._id
            node_id = self.add_node(start_id, coordinates)
            nodes_dict[start_id] = node_id

            end = attributes[1]._end_node
            coordinates = self.convert_coords(end['coords_27700'])
            end_id = end._id
            node_id = self.add_node(end_id, coordinates)
            nodes_dict[end_id] = node_id

        return nodes_dict

    def create_links(self, graph, nodes_dict):
        """
        Create links (pipes and valves) from Neo4j graph data.

        Parameters:
            graph (list): List of results from Neo4j query.
            nodes_dict (dict): Dictionary mapping Neo4j node IDs to WNTR node IDs.
        """
        for attributes in graph:
            start = attributes[1]._start_node
            start_id = start._id
            start_node_id = nodes_dict[start_id]

            end = attributes[1]._end_node
            end_id = end._id
            end_node_id = nodes_dict[end_id]

            edge_id = attributes[1]._id
            diameter = attributes[1].get('diameter', 0.1)  # Default diameter
            length = attributes[1].get('segment_length', 1.0)  # Default length
            roughness = self.roughness_values.get(attributes[1].get('material'), 120)

            if "OperationalSite" in end.labels:
                base_head = 20.0  # Example base head
                self.wn.add_reservoir(end_node_id, base_head=base_head, coordinates=self.convert_coords(end['coords_27700']))
            elif "NetworkOptValve" in end.labels or "PressureControlValve" in end.labels:
                connected_nodes, diameter = self.get_connected_nodes(start)
                valve_type = np.random.choice(self.valve_types)
                if len(connected_nodes) == 2:
                    self.wn.add_valve(end_node_id, connected_nodes[0], connected_nodes[1], diameter, valve_type)
            else:
                self.add_pipe(edge_id, start_node_id, end_node_id, diameter, length, roughness)

    def transform_junction_with_assets(self, graph):
        """
        Transform junctions with connected assets into appropriate WNTR elements.

        Parameters:
            graph (list): List of results from Neo4j query.
        """
        for attributes in graph:
            start = attributes[1]._start_node
            end = attributes[1]._end_node

            # Check if the start or end node has an asset
            start_asset = db.cypher_query(f"MATCH (n)-[r:HAS_ASSET]->(a) WHERE id(n)={start._id} RETURN a")[0]
            end_asset = db.cypher_query(f"MATCH (n)-[r:HAS_ASSET]->(a) WHERE id(n)={end._id} RETURN a")[0]

            # Process start node with asset
            if start_asset:
                self.process_asset(start, start_asset[0][0])

            # Process end node with asset
            if end_asset:
                self.process_asset(end, end_asset[0][0])

    def process_asset(self, junction, asset):
        """
        Convert a junction with a connected asset to the corresponding WNTR element.

        Parameters:
            junction (neomodel Node): Junction node to be processed.
            asset (neomodel Node): Connected asset node to be converted.
        """
        junction_id = self.generate_unique_id(junction._id)

        if "OperationalSite" in asset.labels:
            base_head = 20.0  # Example base head
            coordinates = junction['coords_27700']
            self.wn.add_reservoir(junction_id, base_head=base_head, coordinates=coordinates)
        elif "NetworkOptValve" in asset.labels or "PressureControlValve" in asset.labels:
            # Find connected nodes to replace the junction with a valve
            connected_nodes, diameter = self.get_connected_nodes(junction)
            valve_type = np.random.choice(self.valve_types)
            if len(connected_nodes) == 2:
                self.wn.add_valve(junction_id, connected_nodes[0], connected_nodes[1], diameter, valve_type)

    def wntr_to_inp(self):
        """
        Exports the WNTR model to an INP (EPANET input file) format.
        """
        wntr.network.write_inpfile(self.wn, filename=self.config.outputfile)

    def wntr_to_json(self, filename):
        """
        Exports the WNTR model to a JSON format.

        Parameters:
            filename (str): Name of the JSON file to export.
        """
        wntr.network.write_json(self.wn, filename=self.config.outputfile)
