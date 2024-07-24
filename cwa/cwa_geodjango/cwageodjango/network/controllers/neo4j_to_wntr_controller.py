
from neomodel import db
from cleanwater.transform import Neo4j2Wntr
import wntr


class Convert2Wntr(Neo4j2Wntr):
    """
    Class for converting Neo4j graph data to Water Network Toolkit (WNTR) format.

    Inherits from Neo4j2Wntr class.

    Parameters:
        config: Configuration object containing settings for the conversion.

    Attributes:
        config: Configuration object containing settings for the conversion.
    """

    def __init__(self, config, dma=None):
        super().__init__(config)
        self.dma = dma
        self.links_loaded = set()
        self.nodes_loaded = set()
        self.asset_dict = {}

    def query_neo4j(self):
        """
        Query the graph database in batches and populate self.nodes_loaded directly.
        """
        offset = 0
        total_nodes_loaded = 0
        utilities = list(set(self.config.utility_names or []))

        conditions = []
        if self.dma:
            print(self.dma)
            conditions.append(f"d.code IN ['{self.dma}']")
        else:
            print("no DMAs found!")
        if utilities:
            utility_names_str = ", ".join(f"'{utility_name}'" for utility_name in utilities)
            conditions.append(f"u.name IN [{utility_names_str}]")

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        node_query_base = """
            MATCH (n)-[r:PipeMain]-(m)
            MATCH (n)-[:IN_DMA]->(d)
            MATCH (n)-[:IN_UTILITY]->(u)
            WHERE {conditions}
            RETURN n,m
            SKIP {offset}
            LIMIT {batch_size}
        """

        edge_query_base = """
            MATCH (n)-[r:PipeMain]->(m)
            MATCH (n)-[:IN_DMA]->(d)
            MATCH (m)-[:IN_DMA]->(d)
            MATCH (n)-[:IN_UTILITY]->(u)
            MATCH (m)-[:IN_UTILITY]->(u)
            WHERE {conditions}
            RETURN r
            SKIP {offset}
            LIMIT {batch_size}
        """

        while total_nodes_loaded < self.config.query_limit:
            try:
                node_query = node_query_base.format(
                    conditions=where_clause,
                    offset=offset,
                    batch_size=self.config.batch_size
                )

                edge_query = edge_query_base.format(
                    conditions=where_clause,
                    offset=offset,
                    batch_size=self.config.batch_size
                )

                node_results_raw, _ = db.cypher_query(node_query)
                node_results = self.flatten_list(node_results_raw)
                edge_results_raw, _ = db.cypher_query(edge_query)
                edge_results = self.flatten_list(edge_results_raw)

                offset += self.config.batch_size
            except Exception as e:
                print(f"Error querying the database: {e}")
                break

            if node_results_raw:
                unique_nodes = {node["node_key"] for node in node_results}
                unique_edges = {edge._id for edge in edge_results}

                new_nodes = {record for record in node_results
                             if record['node_key'] not in {node['node_key'] for node in self.nodes_loaded}}
                print(f"Nodes queried: {len(unique_nodes)}, Nodes added: {len(new_nodes)}")
                new_edges = {record for record in edge_results
                             if record.id not in {link.id for link in self.links_loaded}}
                print(f"Edges queried: {len(unique_edges)}, Edges added: {len(new_edges)}")

                self.nodes_loaded.update(new_nodes)
                self.links_loaded.update(new_edges)
                total_nodes_loaded += len(new_nodes)

            else:
                print("Query returned no records")
                break

    def generate_asset_dict(self, node_ids):
        """
        Query Neo4j for assets connected to NetworkNodes.

        Parameters:
            node_ids (list): List of node IDs to filter nodes.

        Returns:
            results: Result object containing node IDs and their asset labels.
        """
        utilities = (self.config.utility_names or [])
        dmas = list(set(self.config.dma_codes))

        base_query = """
            MATCH (n)-[:PipeMain]-(m)
            MATCH (n)-[:IN_UTILITY]->(u)
            MATCH (n)-[:IN_DMA]->(d)
            MATCH (n)-[:HAS_ASSET]->(a)
            WHERE {conditions}
            RETURN id(n) AS node_id, 
                   CASE
                       WHEN a.subtype CONTAINS 'reservoir' THEN 'reservoir'
                       ELSE labels(a)
                   END AS asset_labels
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

        for attributes in results:
            node_id = str(attributes[0])
            node_labels = attributes[1]
            self.asset_dict[node_id] = node_labels

    def convert(self):
        """
        Converts the Neo4j graph data to WNTR format.
        """
        print("Querying Neo4j")
        self.query_neo4j()

        print("Assembling asset dictionary")
        node_ids = [node._id for node in self.nodes_loaded]
        self.generate_asset_dict(node_ids)

        print("Building Water Network")
        self.create_graph()

        print("Checking graph completeness")
        self.check_graph_completeness()

    def create_graph(self):
        """
        Create a WNTR graph from the loaded nodes and links.
        """
        for node in self.nodes_loaded:
            node_id_str = str(node._id)
            coordinates = self.convert_coords(node['coords_27700'])
            node_type = self.asset_dict.get(node_id_str)
            self.add_node(node_id_str, coordinates, node_type)

        for link in self.links_loaded:
            link_id = str(link.id)
            start_node_id = str(link._start_node._id)
            end_node_id = str(link._end_node._id)

            if start_node_id not in self.wn.node_name_list:
                print(f"Missing start node! {start_node_id} for link {link_id}")

            if end_node_id not in self.wn.node_name_list:
                print(f"Missing end node! {end_node_id} for link {link_id}")

            diameter = link["diameter"]
            length = link["segment_length"]
            roughness = self.roughness_values.get(link['material'], 120)
            self.add_pipe(link_id, start_node_id, end_node_id, diameter, length, roughness)

    def wntr_to_inp(self):
        """
        Exports the WNTR model to an INP (EPANET input file) format.
        """
        print(f"Fetched nodes: {len(self.nodes_loaded)}, Fetched links: {len(self.links_loaded)}")
        print(f"WN nodes: {len(self.wn.node_name_list)}, WN links: {len(self.wn.link_name_list)}")

        filename = "WNTR_" + str(self.dma)

        wntr.network.write_inpfile(self.wn, filename)

    def wntr_to_json(self):
        """
        Exports the WNTR model to a JSON format.

        Parameters:
            filename (str): Name of the JSON file to export.
        """
        filename = "WNTR_" + str(self.dma)
        wntr.network.write_json(self.wn, filename)
