import random
from neomodel import db
from cleanwater.transform import Neo4j2Wntr
from cwageodjango.config.settings import sqids
import wntr
from wntr import network


class Convert2Wntr(Neo4j2Wntr):
    """
    Class for converting Neo4j graph data to Water Network Toolkit (WNTR) format.

    Inherits from Neo4j2Wntr class.

    Parameters:
        config: Configuration object containing settings for the conversion.

    Attributes:
        config: Configuration object containing settings for the conversion.

    """

    def __init__(self, config):
        self.config = config
        super().__init__(sqids)

    def query_network_nodes_and_pipes(self, batch_size, utilities, dmas):
        """
        Query Neo4j for NetworkNodes and their PipeMain relationships.

        Parameters:
            batch_size (int): Size of each batch for querying the graph database.
            utilities (list): List of utility names to filter nodes.
            dmas (list): List of DMA codes to filter nodes.

        Returns:
            results: Result object containing network nodes and pipes.
        """
        results, m = db.cypher_query(
            f"MATCH (n:NetworkNode)-[:IN_UTILITY]-(u:Utility), (n)-[:IN_DMA]-(d:DMA) "
            f"WHERE u.name IN {utilities} AND d.code IN {dmas} "
            f"WITH n "
            f"MATCH (n)-[r:PipeMain]-(s:NetworkNode) "
            f"RETURN n, r, s, id(n) AS node_id_n, id(s) AS node_id_s "
            f"LIMIT {batch_size};"
        )
        return results

    def query_assets_for_nodes(self, utilities, dmas):
        """
        Query Neo4j for assets connected to NetworkNodes.

        Parameters:
            utilities (list): List of utility names to filter nodes.
            dmas (list): List of DMA codes to filter nodes.

        Returns:
            results: Result object containing node IDs and their asset labels.
        """
        results, m = db.cypher_query(
            f"MATCH (n:NetworkNode)-[:IN_UTILITY]-(u:Utility), (n)-[:IN_DMA]-(d:DMA) "
            f"WHERE u.name IN {utilities} AND d.code IN {dmas} "
            f"WITH n "
            f"MATCH (n)-[:HAS_ASSET]->(a) "
            f"RETURN id(n) AS node_id, labels(a) AS asset_labels;"
        )
        return results

    def generate_asset_dict(self, graph):
        """
        Generate a dictionary containing node ID and type from the Neo4j query results.

        Parameters:
            graph (list): List of results from Neo4j query.

        Returns:
            asset_dict (dict): Dictionary containing node IDs and their types.
        """
        asset_dict = {}
        for attributes in graph:
            node_id = attributes[0]
            node_labels = attributes[1]

            asset_dict[node_id] = node_labels

        return asset_dict

    def convert(self):
        """
        Converts the Neo4j graph data to WNTR format.
        """
        network_nodes_results = self.query_network_nodes_and_pipes(
            self.config.batch_size, self.config.utilities, self.config.dma_codes
        )
        asset_results = self.query_assets_for_nodes(
            self.config.utilities, self.config.dma_codes
        )

        asset_dict = self.generate_asset_dict(asset_results)
        self.create_graph(network_nodes_results, asset_dict)

    def wntr_to_inp(self):
        """
        Exports the WNTR model to an INP (EPANET input file) format.
        """
        wntr.network.write_inpfile(self.wn, filename=self.config.inpfile)

    def wntr_to_json(self, filename):
        """
        Exports the WNTR model to a JSON format.

        Parameters:
            filename (str): Name of the JSON file to export.

        """
        wntr.network.write_json(self.wn, filename=self.config.outputfile)
