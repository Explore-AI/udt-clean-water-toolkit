import json
from multiprocessing.pool import ThreadPool
from django.db import connections
from django.db.models.query import QuerySet
from django.contrib.gis.geos import Point
from neomodel.contrib.spatial_properties import NeomodelPoint
from neomodel.exceptions import UniqueProperty, ConstraintValidationFailed
from cleanwater.exceptions import (
    InvalidNodeException,
    InvalidPipeException,
)
from ..calculators import GisToNeo4jCalculator
from cwa_geod.core.constants import (
    TRUNK_MAIN__NAME,
    DISTRIBUTION_MAIN__NAME,
    PIPE_END__NAME,
    POINT_ASSET__NAME,
)
from ..models import PointAsset, PipeEnd, initialise_node_labels


class GisToNeo4jController(GisToNeo4jCalculator):
    """Create a Neo4J graph of assets from a geospatial
    network of assets"""

    def __init__(self, config):
        self.config = config
        initialise_node_labels()
        super().__init__(config)

    def create_network(self):
        from timeit import default_timer as timer

        start = timer()

        pipes_qs = self.get_pipe_and_asset_data()

        query_offset, query_limit = self._get_query_offset_limit(pipes_qs)

        for offset in range(query_offset, query_limit, self.config.batch_size):
            limit = offset + self.config.batch_size

            print(offset, limit)
            sliced_qs = list(pipes_qs[offset:limit])

            self.calc_pipe_point_relative_positions(sliced_qs)

            self._create_neo4j_graph()

        end = timer()
        print(end - start)

    def create_network_parallel(self):
        from timeit import default_timer as timer

        start = timer()

        pipes_qs = self.get_pipe_and_asset_data()

        query_offset, query_limit = self._get_query_offset_limit(pipes_qs)

        for offset in range(query_offset, query_limit, self.config.batch_size):
            limit = offset + self.config.batch_size
            print(offset, limit)

            sliced_qs = list(pipes_qs[offset:limit])

            self.calc_pipe_point_relative_positions_parallel(sliced_qs)

            self._create_neo4j_graph_parallel()

        end = timer()
        print(end - start)
