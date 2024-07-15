from .base_gis_to_graph_controller import BaseGisToGraphController
from ..calculators import GisToNeo4jCalculator
from ..models import initialise_node_labels


class GisToNeo4jController(BaseGisToGraphController, GisToNeo4jCalculator):
    """Create a Neo4J graph of assets from a geospatial
    network of assets"""

    def __init__(self, config):
        self.config = config
        initialise_node_labels()
        super().__init__(self.config)
        super(BaseGisToGraphController, self).__init__(self.config)

    def create_network(self):
        self.run_calc()

    def create_network_parallel(self):

        print(f"Start parallel run with {self.config.processor_count} cores.")

        self.create_network()
