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
    """

    def __init__(self, config):
        super().__init__(sqids)
        self.config = config
        self.links_loaded = []
        self.nodes_loaded = []
        self.asset_dict = {}

    def query_neo4j(self):
        """
        Query the graph database in batches and populate self.nodes_loaded directly.
        """
        offset = 0
        total_nodes_loaded = 0
        utilities = list(set((self.config.utility_names or [])))
        dmas = list(set(self.config.dma_codes))

        conditions = []
        if dmas:
            dma_codes_str = ", ".join(f"'{dma_code}'" for dma_code in dmas)
            conditions.append(f"dn.code IN [{dma_codes_str}]")

        if utilities:
            utility_names_str = ", ".join(f"'{utility_name}'" for utility_name in utilities)
            conditions.append(f"un.name IN [{utility_names_str}]")

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        node_query_base = """
            MATCH (n)-[r:PipeMain]->(m)
            MATCH (n)-[:IN_DMA]->(dn)
            MATCH (n)-[:IN_UTILITY]->(un)
            WHERE {conditions}
            RETURN n,m
            SKIP {offset}
            LIMIT {batch_size}
        """

        edge_query_base = """
            MATCH (n)-[r:PipeMain]->(m)
            MATCH (n)-[:IN_DMA]->(dn)
            MATCH (n)-[:IN_UTILITY]->(un)
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

                node_results, _ = db.cypher_query(node_query)
                edge_results, _ = db.cypher_query(edge_query)
                offset += self.config.batch_size
            except Exception as e:
                print(f"Error querying the database: {e}")
                break

            node_results = self.flatten_list(node_results)
            edge_results = self.flatten_list(edge_results)

            new_nodes = [record for record in node_results if
                         record['node_key'] not in {node['node_key'] for node in self.nodes_loaded}]
            new_edges = [record for record in edge_results if
                         record.id not in {link.id for link in self.links_loaded}]

            self.nodes_loaded.extend(new_nodes)
            self.links_loaded.extend(new_edges)
            total_nodes_loaded += len(new_nodes)

            if not new_nodes:
                print("Query returned no records")
                break

            print(f"Loaded {len(self.nodes_loaded)} unique nodes")

    def query_assets_for_nodes(self, node_ids):
        """
        Query Neo4j for assets connected to NetworkNodes.

        Parameters:
            node_ids (list): List of node IDs to filter nodes.

        Returns:
            results: Result object containing node IDs and their asset labels.
        """
        utilities = self.config.utility_names or []
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
        for subgraph in graph:
            for attributes in subgraph:
                node_id = attributes[0]
                node_labels = attributes[1]
                self.asset_dict[node_id] = node_labels

    def convert(self):
        """
        Converts the Neo4j graph data to WNTR format.
        """
        # Query the Neo4j database and process nodes and links in batches
        self.query_neo4j()

        # Query assets for the loaded nodes
        node_ids = [node._id for node in self.nodes_loaded]
        asset_results = self.query_assets_for_nodes(node_ids)
        self.generate_asset_dict(asset_results)

        # Create the WNTR graph
        self.create_graph()

    def create_graph(self):
        """
        Create a WNTR graph from the loaded nodes and links.
        """
        for node in self.nodes_loaded:
            coordinates = self.convert_coords(node['coords_27700'])
            self.add_node(node._id, coordinates)

        for link in self.links_loaded:
            link_id = link.id
            start_node_id = link._start_node._id
            end_node_id = link._end_node._id

            if str(start_node_id) not in self.wn.node_name_list:
                print(f"Missing start node! {start_node_id} for link {link_id}")

            if str(end_node_id) not in self.wn.node_name_list:
                print(f"Missing end node! {end_node_id} for link {link_id}")

            diameter = link["diameter"]
            length = link["segment_length"]
            # roughness = self.roughness_values.get(link['material'].lower())
            self.add_pipe(link_id, start_node_id, end_node_id, diameter, length)

    def wntr_to_inp(self):
        """
        Exports the WNTR model to an INP (EPANET input file) format.
        """
        print(f"Fetched nodes: {len(self.nodes_loaded)}, Fetched links: {len(self.links_loaded)}")
        print(f"WN nodes: {len(self.wn.node_name_list)}, WN links: {len(self.wn.link_name_list)}")

        wntr.network.write_inpfile(self.wn, filename=self.config.inpfile)

    def wntr_to_json(self, filename):
        """
        Exports the WNTR model to a JSON format.

        Parameters:
            filename (str): Name of the JSON file to export.
        """
        wntr.network.write_json(self.wn, filename=self.config.outputfile)
