import pdb
import random  # Remove if not used
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
        super().__init__(sqids)
        self.config = config
        self.links_loaded = []
        self.nodes_loaded = []

    def query_network_triads(self):
        """
        Generator function to query the graph database in batches.

        Yields:
            results: Result object containing batched query results.
        """
        offset = 0
        total_loaded = 0
        utilities = list(set((self.config.utility_names or []) + (self.config.utilities or [])))
        dmas = list(set(self.config.dma_codes))

        while total_loaded < self.config.query_limit:
            try:
                base_query = """
                    MATCH (n)-[r:PipeMain]->(m)
                    MATCH (n)-[:IN_DMA]->(dn)
                    MATCH (m)-[:IN_DMA]->(dm)
                    MATCH (n)-[:IN_UTILITY]->(un)
                    MATCH (m)-[:IN_UTILITY]->(um)
                    WHERE {conditions}
                    RETURN n, r, m
                    SKIP {offset}
                    LIMIT {batch_size}
                """
                conditions = []
                if dmas:
                    dma_codes_str = ", ".join(f"'{dma_code}'" for dma_code in dmas)
                    conditions.append(f"dn.code IN [{dma_codes_str}] AND dm.code IN [{dma_codes_str}]")

                if utilities:
                    utility_names_str = ", ".join(f"'{utility_name}'" for utility_name in utilities)
                    conditions.append(f"un.name IN [{utility_names_str}] AND um.name IN [{utility_names_str}]")

                where_clause = " AND ".join(conditions) if conditions else "1=1"
                query = base_query.format(conditions=where_clause, offset=offset, batch_size=self.config.batch_size)

                print("Retrieving data")
                results, meta = db.cypher_query(query)
                offset += self.config.batch_size
            except Exception as e:
                print(f"Error querying the database: {e}")
                break

            records = list(results)
            total_loaded += len(records)

            if not records:
                print("Query returned no records")
                break

            print(f"Loaded {total_loaded}")

            node_keys = {node['node_key'] for node in self.nodes_loaded}
            links_ids = {link.id for link in self.links_loaded}

            for record in records:
                if record[0]['node_key'] not in node_keys:
                    self.nodes_loaded.append(record[0])
                    node_keys.add(record[0]['node_key'])
                if record[2]['node_key'] not in node_keys:
                    self.nodes_loaded.append(record[2])
                    node_keys.add(record[2]['node_key'])
                if record[1].id not in links_ids:
                    self.links_loaded.append(record[1])
                    links_ids.add(record[1].id)

            yield results

    def query_assets_for_nodes(self, node_ids):
        """
        Query Neo4j for assets connected to NetworkNodes.

        Parameters:
            node_ids (list): List of node IDs to filter nodes.

        Returns:
            results: Result object containing node IDs and their asset labels.
        """
        utilities = (self.config.utility_names or []) + (self.config.utilities or [])
        dmas = self.config.dma_codes

        base_query = """
            MATCH (n:NetworkNode)-[:IN_UTILITY]-(u:Utility)
            MATCH (n)-[:IN_DMA]-(d:DMA)
            MATCH (n)-[:HAS_ASSET]->(a)
            WHERE {conditions}
            RETURN id(n) AS node_id, labels(a) AS asset_labels
        """
        conditions = [f"id(n) IN [{', '.join(map(str, node_ids))}]"]

        if utilities:
            utility_names_str = ", ".join(f"'{utility_name}'" for utility_name in utilities)
            conditions.append(f"u.name IN [{utility_names_str}]")

        if dmas:
            dma_codes_str = ", ".join(f"'{dma_code}'" for dma_code in dmas)
            conditions.append(f"d.code IN [{dma_codes_str}]")

        where_clause = " AND ".join(conditions)
        query = base_query.format(conditions=where_clause)

        try:
            print("Querying assets")
            results, _ = db.cypher_query(query)
        except Exception as e:
            print(f"Error querying assets: {e}")
            results = []

        yield results

    def generate_asset_dict(self, graph):
        """
        Generate a dictionary containing node ID and type from the Neo4j query results.

        Parameters:
            graph (list): List of results from Neo4j query.

        Returns:
            asset_dict (dict): Dictionary containing node IDs and their types.
        """
        asset_dict = {}
        for subgraph in graph:
            for attributes in subgraph:
                node_id = attributes[0]
                node_labels = attributes[1]
                asset_dict[node_id] = node_labels
        return asset_dict

    def convert(self):
        """
        Converts the Neo4j graph data to WNTR format.
        """
        network_triads_results = self.query_network_triads()
        node_ids = [node._id for node in self.nodes_loaded]
        asset_results = self.query_assets_for_nodes(node_ids)
        asset_dict = self.generate_asset_dict(asset_results)

        for subgraph in network_triads_results:
            self.create_graph(subgraph, asset_dict)

    def wntr_to_inp(self):
        """
        Exports the WNTR model to an INP (EPANET input file) format.
        """
        print(f"fetched nodes: {len(self.nodes_loaded)}, fetched links: {len(self.links_loaded)}")
        print(f"WN nodes: {len(self.wn.node_name_list)}, WN links: {len(self.wn.link_name_list)}")

        wntr.network.write_inpfile(self.wn, filename=self.config.inpfile)

    def wntr_to_json(self, filename):
        """
        Exports the WNTR model to a JSON format.

        Parameters:
            filename (str): Name of the JSON file to export.
        """
        wntr.network.write_json(self.wn, filename=self.config.outputfile)
