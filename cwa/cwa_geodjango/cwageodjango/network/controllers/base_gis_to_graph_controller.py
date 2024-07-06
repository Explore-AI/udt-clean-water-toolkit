from django.db.models.query import QuerySet
from cwageodjango.assets.controllers import PipeMainsController


class BaseGisToGraphController:
    """This is an Abstract Base Class"""

    def __init__(self, config):
        self.config = config

    def run_calc(self):

        pipes_qs, pipes_pks = self._get_pipe_and_asset_data()

        query_offset, query_limit = self._get_query_offset_limit(pipes_pks)

        for offset in range(query_offset, query_limit, self.config.batch_size):
            # limit = offset + self.config.batch_size
            from timeit import default_timer as timer

            t0 = timer()

            start_pk = pipes_pks[offset]

            print(offset, offset + self.config.batch_size)

            qs = pipes_qs.filter(pk__gte=start_pk)[: self.config.batch_size]

            qs_data = list(qs)

            t1 = timer()
            print("qs", t1 - t0)

            if self.config.parallel:
                # defined in child class
                self.calc_pipe_point_relative_positions_parallel(qs_data)
            else:
                # defined in child class
                self.calc_pipe_point_relative_positions(qs_data)

            qs = []
            t2 = timer()
            print("calc", t2 - t1)

            self.create_neo4j_graph()
            t3 = timer()
            print("create", t3 - t2)

            end = timer()
            print(end - t0)

    def _get_query_offset_limit(self, pipes_pks):

        pipe_count = len(pipes_pks)

        if not self.config.query_limit:
            query_limit = pipe_count
        elif self.config.query_offset + self.config.query_limit == pipe_count:
            query_limit = pipe_count
        else:
            query_limit = self.config.query_offset + self.config.query_limit

        if not self.config.query_offset:
            query_offset = 0
        else:
            query_offset = self.config.query_offset

        return query_offset, query_limit

    # This fn is a candidate to be abstracted out into the NetworkController
    def _get_pipe_and_asset_data(self) -> QuerySet:

        filters = {"dma_codes": self.config.dma_codes}

        pipes_qs: QuerySet = self.get_mains_data(filters)

        return pipes_qs

    def get_mains_data(self, filters={}) -> QuerySet:
        pm: PipeMainsController = PipeMainsController()
        return pm.get_pipe_point_relation_queryset(filters), pm.get_mains_pks(filters)
