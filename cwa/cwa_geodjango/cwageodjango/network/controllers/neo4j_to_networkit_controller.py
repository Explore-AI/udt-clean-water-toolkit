import networkit as nk
from neomodel import db
from cleanwater.controllers.networkit_controller import Neo4j2Networkit


class Convert2Networkit(Neo4j2Networkit):
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
            results, m = db.cypher_query(
                f"MATCH (n)-[r]->(m) RETURN n, r, m limit {batch_size}"
            )
            records = list(results)
            if not records:
                break

            yield results
            offset += batch_size

            if len(records) <= batch_size:
                break

    def convert(self):
        """
        Converts the Neo4j graph data to NetworKit format.
        Conversion is done in batches.
        """

        for graph in self.query_graph(self.config.batch_size):
            self.convert_neo4j_to_nk(graph)

    def export_graphml(self):
        nk.writeGraph(self.G, self.config.outputfile, nk.Format.GML)
