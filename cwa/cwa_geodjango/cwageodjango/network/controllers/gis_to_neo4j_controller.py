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


from collections import OrderedDict
from cwageodjango.config.settings import sqids
from cwageodjango.assets.models import *
from cleanwater.transform.network_transform import NetworkTransform


# BaseGisToGraphController, GisToNeo4jCalculator
class GisToNeo4jController2:
    """Create a Neo4J graph of assets from a geospatial
    network of assets"""

    def __init__(self, config):
        self.config = config
        initialise_node_labels()
        # super().__init__(self.config)
        # super(BaseGisToGraphController, self).__init__(self.config)

    def create_network(self):

        point_asset_models = OrderedDict(
            [("logger", Logger), ("hydrant", Hydrant), ("network_meter", NetworkMeter)]
        )

        filters = {
            "utility_names": self.config.utility_names,
            "dma_codes": self.config.dma_codes,
        }

        nt = NetworkTransform()
        nt.initialise(
            "gis2neo4j",
            pipe_asset=PipeMain,
            point_assets=point_asset_models,
            filters=filters,
        )

        nt.run(srid=27700, sqids=sqids, gis_framework="geodjango")
        print("aaaaa")
        import pdb

        pdb.set_trace()

    def create_network_parallel(self):

        print(f"Start parallel run with {self.config.processor_count} cores.")

        self.create_network()
