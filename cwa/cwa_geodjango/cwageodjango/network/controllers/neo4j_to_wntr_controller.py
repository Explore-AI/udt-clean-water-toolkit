from neomodel import db
from cleanwater.transform import Neo4j2Wntr
from cleanwater.data_managers import NetworkDataManager
from cwageodjango.config.settings import sqids

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

            if len(records) <= batch_size:
                break
            
    def convert(self):
        """
        Converts the Neo4j graph data to WNTR format.

        """
        for sub_graph in self.query_graph(self.config.batch_size):
            self.create_graph(sub_graph)

