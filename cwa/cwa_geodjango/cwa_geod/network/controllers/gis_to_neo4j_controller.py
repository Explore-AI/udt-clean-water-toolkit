from django.db.models.query import QuerySet
from cleanwater.controllers.network_controller import NetworkController
from ..calculators import GisToNeo4jCalculator
from ..models import initialise_node_labels
from cwa_geod.assets.controllers import (
    TrunkMainsController,
    DistributionMainsController,
)


class GisToNeo4jController(NetworkController, GisToNeo4jCalculator):
    """Create a Neo4J graph of assets from a geospatial
    network of assets"""

    def __init__(self, config):
        self.config = config
        initialise_node_labels()
        NetworkController.__init__(self, self.config.srid)
        GisToNeo4jCalculator.__init__(self, self.config)

    def create_network(self):
        from timeit import default_timer as timer

        start = timer()

        pipes_qs = self._get_pipe_and_asset_data()

        query_offset, query_limit = self._get_query_offset_limit(pipes_qs)

        for offset in range(query_offset, query_limit, self.config.batch_size):
            limit = offset + self.config.batch_size

            print(offset, limit, "a")
            sliced_qs = list(pipes_qs[offset:limit])

            self.calc_pipe_point_relative_positions(sliced_qs)

            self.create_neo4j_graph()

        end = timer()
        print(end - start)

    def create_network_parallel(self):
        from timeit import default_timer as timer

        start = timer()

        pipes_qs = self._get_pipe_and_asset_data()

        query_offset, query_limit = self._get_query_offset_limit(pipes_qs)

        for offset in range(query_offset, query_limit, self.config.batch_size):
            limit = offset + self.config.batch_size
            print(offset, limit)

            t0 = timer()

            sliced_qs = list(pipes_qs[offset:limit])
            t1 = timer()
            print("qs", t1 - t0)


            self.calc_pipe_point_relative_positions_parallel(sliced_qs)
            t2 = timer()
            print("calc", t2 - t1)


            self._create_neo4j_graph_parallel()
            t3 = timer()
            print("create", t3 - t2)

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

    # This fn is a candidate to be abstracted out into the NetworkController
    def _get_pipe_and_asset_data(self) -> QuerySet:
        trunk_mains_qs: QuerySet = self.get_trunk_mains_data()
        distribution_mains_qs: QuerySet = self.get_distribution_mains_data()

        pipes_qs = trunk_mains_qs.union(distribution_mains_qs, all=True)
        return pipes_qs

    def get_trunk_mains_data(self) -> QuerySet:
        tm: TrunkMainsController = TrunkMainsController()
        return tm.get_pipe_point_relation_queryset()

    def get_distribution_mains_data(self) -> QuerySet:
        dm: DistributionMainsController = DistributionMainsController()
        return dm.get_pipe_point_relation_queryset()
