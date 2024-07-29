from ..constants import POINT_ASSET_MODELS, PIPE_MAIN_MODEL
from cleanwater.transform.network_transform import NetworkTransform


class GisToNxController(GisToNx):
    """Create a Neo4J graph of assets from a geospatial
    network of assets"""

    def __init__(self, config):
        self.config = config
        super().__init__(self.config)

    def create_network(self):
        filters = {
            "utility_names": self.config.utility_names,
            "dma_codes": self.config.dma_codes,
        }

        nt = NetworkTransform()

        nt.initialise(
            "gis2nx",
            pipe_asset=PIPE_MAIN_MODEL,
            point_assets=POINT_ASSET_MODELS,
            filters=filters,
        )

        nt.run(
            27700,
            sqids,
            gis_framework="geodjango",
            batch_size=self.config.batch_size,
            query_limit=self.config.query_limit,
            query_offset=self.config.query_offset,
        )
