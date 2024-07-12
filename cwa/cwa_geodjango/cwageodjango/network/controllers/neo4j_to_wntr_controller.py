import pdb
import numpy as np
import wntr
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
        nx_graph: NetworkX directed graph representation of the network.
    """

    def __init__(self, config):
        super().__init__(sqids)
        self.config = config
        self.all_nodes = set()
        self.all_edges = set()
        self.valve_types = ['PRV', 'PSV', 'FCV', 'TCV']  # Example valve types
        self.wn = wntr.network.WaterNetworkModel()  # Initialize WNTR model

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
            try:
                if self.config.dma_codes:  # Check if there are any DMA codes specified
                    dma_codes_str = ", ".join(f"'{dma_code}'" for dma_code in self.config.dma_codes)
                    query = f"""
                        MATCH (n)-[r:PipeMain]-(m), (n)-[:IN_DMA]->(d), (m)-[:IN_DMA]->(d)
                        WHERE d.code IN [{dma_codes_str}]
                        WITH n, m, COLLECT(r) AS edges
                        UNWIND edges AS edge
                        WITH n, m, edge
                        ORDER BY id(edge) // Optional: Choose which edge to keep based on certain criteria
                        WITH n, m, COLLECT(edge)[0] AS uniqueEdge
                        RETURN n, uniqueEdge, m
                        SKIP {offset}
                        LIMIT {batch_size}
                        """

                else:
                    query = f"""                    
                            MATCH (n)-[r:PipeMain]-(m)
                            WITH n, m, COLLECT(r) AS edges
                            UNWIND edges AS edge
                            WITH n, m, edge
                            ORDER BY id(edge) // Optional: Choose which edge to keep based on certain criteria
                            WITH n, m, COLLECT(edge)[0] AS uniqueEdge
                            RETURN n, uniqueEdge, m
                            SKIP {offset}
                            LIMIT {batch_size}
                            """

                results, meta = db.cypher_query(query)
                offset += batch_size
            except Exception as e:
                print(f"Error querying the database: {e}")
                break

            records = list(results)
            total_loaded += len(records)

            if not records:
                break

            print("Loaded", total_loaded)
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

        print("Processing nodes")
        self.all_nodes = set(self.remove_duplicate_nodes(list(self.all_nodes)))
        for node in self.all_nodes:
            self.create_nodes_and_assets(node)

        num_nodes = len(self.all_nodes)
        num_wntr_nodes = len(self.wn.node_name_list)

        print("Processing edges")
        self.create_links_and_assets()

        num_edges = len(self.all_edges)
        num_wntr_edges = len(self.wn.link_name_list)

        print("Total nodes queried:", num_nodes)
        print("Total nodes in WNTR model:", num_wntr_nodes)
        print("Total edges queried:", num_edges)
        print("Total edges in WNTR model:", num_wntr_edges)

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
            self.add_junction(node_id, coordinates)



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

            if self.is_valve(end_node._id):
                valve_type = np.random.choice(self.valve_types)
                valve_id = self.generate_unique_id(edge._id)
                self.add_valve(valve_id, start_node_id, end_node_id, diameter, valve_type)
            else:
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

    @staticmethod
    def remove_duplicate_nodes(node_list):
        """
        Remove duplicate nodes from a list of nodes.

        Parameters:
            node_list (list of dict): List of nodes to remove duplicates from.

        Returns:
            list: List of nodes with duplicates removed.
        """
        seen_nodes = []
        result = []

        for node in node_list:
            if node not in seen_nodes:
                seen_nodes.append(node)
                result.append(node)

        return result
