import argparse
from cleanwater.controllers.wntr_controller import Neo4j2Wntr
import wntr
from wntr import network
from neomodel import db

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
        super().__init__()

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
            results, m = db.cypher_query(f"MATCH (n)-[r]-(m) RETURN n, r, m limit {batch_size}")
            records = list(results)
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
        for batch_result in self.query_graph(self.config.batch_size):
            self._process_batch(batch_result)

    def export_inp(self):
        """
        Exports the WNTR model to an INP (EPANET input file) format.

        """
        wntr.network.write_inpfile(self.wn, filename=self.config.outputfile)

    def export_json(self, filename):
        """
        Exports the WNTR model to a JSON format.

        Parameters:
            filename (str): Name of the JSON file to export.

        """
        wntr.network.write_json(self.wn, path_or_buf=self.config.outputfile)