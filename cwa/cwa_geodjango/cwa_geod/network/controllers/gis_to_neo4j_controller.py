from ..calculators import GisToNeo4jCalculator
from ..models import initialise_node_labels


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

            print(offset, limit, "a")
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


    def _get_query_offset_limit(self, pipes_qs):
        pipe_count = self.get_pipe_count(pipes_qs)

        if not self.config.query_limit or self.config.query_limit == pipe_count:
            query_limit = pipe_count
        else:
            query_limit = self.config.query_limit

        if not self.config.query_offset:
            query_offset = 0
        else:
            query_offset = self.config.query_offset

        return query_offset, query_limit
