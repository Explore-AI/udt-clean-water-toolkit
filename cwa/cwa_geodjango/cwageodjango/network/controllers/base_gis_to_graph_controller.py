from django.db.models.query import QuerySet
from cwageodjango.assets.controllers import (
    ConnectionMainsController,
    TrunkMainsController,
    DistributionMainsController,
)


class BaseGisToGraphController:
    """Create a Neo4J graph of assets from a geospatial
    network of assets"""

    def __init__(self, config):
        self.config = config

    def create_network(self):
        from timeit import default_timer as timer

        start = timer()

        pipes_filtered_qs, pipes_filterd_pks = self._get_pipe_and_asset_data()

        for pipe_qs, pipe_pks in zip(pipes_filtered_qs, pipes_filterd_pks):

            for i, start_index in enumerate(
                range(
                    0,
                    len(pipe_pks),
                    self.config.batch_size,
                ),
                start=1,
            ):
                t0 = timer()

                start_pk = pipe_pks[start_index]

                if (start_index + self.config.batch_size) < len(pipe_pks):
                    end_pk = pipe_pks[self.config.batch_size * i]
                else:
                    end_pk = pipe_pks[-1]

                print(start_pk, end_pk)
                sliced_qs = list(pipe_qs.filter(pk__gte=start_pk, pk__lt=end_pk))
                t1 = timer()
                print("qs", t1 - t0)

                if self.config.parallel:
                    self.calc_pipe_point_relative_positions_parallel(sliced_qs)
                else:
                    self.calc_pipe_point_relative_positions(sliced_qs)

                sliced_qs = []
                t2 = timer()
                print("calc", t2 - t1)

                self.create_neo4j_graph()
                t3 = timer()
                print("create", t3 - t2)

                end = timer()
                print(end - start)

    def create_network_parallel(self):

        print(f"Start parallel run with {self.config.processor_count} cores.")

        super().create_network()

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

        filters = {"dma_codes": self.config.dma_codes}

        trunk_mains_qs, trunk_mains_pks = self.get_trunk_mains_data(filters)
        distribution_mains_qs, distribution_mains_pks = (
            self.get_distribution_mains_data(filters)
        )
        connection_mains_qs, connection_mains_pks = self.get_connection_mains_data(
            filters
        )

        pipes_pks = [trunk_mains_pks, distribution_mains_pks, connection_mains_pks]
        pipes_qs = [trunk_mains_qs, distribution_mains_qs, connection_mains_qs]

        pipes_filterd_pks = []
        pipes_filtered_qs = []

        offset = self.config.query_offset
        limit = self.config.query_limit

        for pipe_pks, qs in zip(pipes_pks, pipes_qs):
            mains_count = len(pipe_pks)

            if offset <= mains_count:
                gte_pk = pipe_pks[offset]
            else:
                gte_pk = pipe_pks[-1]

            if limit < mains_count:
                lt_pk = pipe_pks[limit]
            else:
                lt_pk = pipe_pks[-1]

            pipes_filterd_pks.append(
                list(
                    filter(
                        lambda x: False if ((x >= lt_pk) or (x < gte_pk)) else True,
                        pipe_pks,
                    )
                )
            )
            pipes_filtered_qs.append(qs.filter(pk__gte=gte_pk, pk__lt=lt_pk))

            offset = 0
            if limit >= mains_count:
                limit = limit - mains_count
            else:
                break

        return pipes_filtered_qs, pipes_filterd_pks

    def get_trunk_mains_data(self, filters={}) -> QuerySet:
        tm: TrunkMainsController = TrunkMainsController()
        return tm.get_pipe_point_relation_queryset(filters), tm.get_mains_pks(filters)

    def get_distribution_mains_data(self, filters={}) -> QuerySet:
        dm: DistributionMainsController = DistributionMainsController()
        return dm.get_pipe_point_relation_queryset(filters), dm.get_mains_pks(filters)

    def get_connection_mains_data(self, filters={}) -> QuerySet:
        cm: ConnectionMainsController = ConnectionMainsController()
        return cm.get_pipe_point_relation_queryset(filters), cm.get_mains_pks(filters)
