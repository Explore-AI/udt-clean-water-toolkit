import argparse
from cleanwater.controllers.wntr_controller import Neo4j2Wntr
import wntr
from wntr import network
from neomodel import db

class Convert2Wntr(Neo4j2Wntr):
    def __init__(self):
        super().__init__()

    def query_graph(self, batch_size):    
        offset = 0
        while True:
            results, m = db.cypher_query(f"MATCH (n)-[r]-(m) RETURN n, r, m limit {batch_size}")
            records = list(results)  # Fetch all records from the result
            if not records:
                break  # No more records to fetch

            yield results  # Yield the result object
            offset += batch_size  # Increment offset for next batch

            if len(records) < batch_size:
                break  # Last batch fetched

    def convert(self, batch_size):
        for batch_result in self.query_graph(batch_size):
            self._process_batch(batch_result)

    def export_inp(self, filename):
        wntr.network.write_inpfile(self.wn, filename=filename)

    def export_json(self, filename):
        wntr.network.write_json(self.wn, path_or_buf=filename)