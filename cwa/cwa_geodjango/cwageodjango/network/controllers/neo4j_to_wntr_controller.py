from neomodel import db
from cleanwater.transform import Neo4j2Wntr
from cwageodjango.config.settings import sqids
import numpy as np
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
        self.config = config
        self.valve_types = ['PRV', 'PSV', 'FCV', 'TCV']  # Example valve types
        super().__init__(sqids)


    def query_graph(self, batch_size):
        """
        Generator function to query the graph database in batches.

        Parameters:
            batch_size (int): Size of each batch for querying the graph database.

        Yields:
            results: Result object containing batched query results.
        """
        offset = 0
        while True:
            results, meta = db.cypher_query(
                f"MATCH (n)-[r]-(m) RETURN n, r, m LIMIT {batch_size} SKIP {offset}"
            )
            records = list(results)
            if not records:
                break

            yield results
            offset += batch_size

            if len(records) < batch_size:
                break

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
        asset_label = list(asset.labels)[0]

        if asset_label == "OperationalSite":
            base_head = 20.0  # Example base head
            coordinates = junction['coords_27700']
            self.wn.add_reservoir(junction_id, base_head=base_head, coordinates=coordinates)
        elif asset_label == "NetworkOptValve" or asset_label == "PressureControlValve":
            # Find connected nodes to replace the junction with a valve
            connected_nodes, diameter = self.get_connected_nodes(junction)
            valve_type = np.random.choice(self.valve_types)
            if len(connected_nodes) == 2:
                self.wn.add_valve(junction_id, connected_nodes[0], connected_nodes[1], diameter, valve_type)

    def get_connected_nodes(self, node):
        """
        Get the IDs of nodes connected to the given node, excluding any nodes that are assets.

        Parameters:
            node (neomodel Node): Node to find connected nodes for.

        Returns:
            connected_node_ids (list): List of connected node IDs.
        """
        results, _ = db.cypher_query(f"MATCH (n)-[r:PIPE]-(m) WHERE id(n)={node._id} RETURN m")
        return [self.generate_unique_id(n._id) for n in results[0] if 'Asset' not in n.labels], results[0].diameter

    def convert(self):
        """
        Converts the Neo4j graph data to WNTR format.
        """
        for sub_graph in self.query_graph(self.config.batch_size):
            self.transform_junction_with_assets(sub_graph)
            self.create_graph(sub_graph)

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