from django.db.models.query import QuerySet
import networkit as nk
from cleanwater.transform import GisToNk
from cwageodjango.assets.controllers import PipeMainsController


class GisToNkController(GisToNk):
    """
    Create a NetworKit graph of assets from a geospatial
    network of assets

    """

    def __init__(self, config):
        self.config = config
        super().__init__(self.config)

    def create_network(self):
        """
        Create a network graph from geospatial asset data.

        Retrieves pipe and asset data from the database in batches, calculates relative positions
        of pipes, and creates a network graph using Networkit.

        """
        from timeit import default_timer as timer

        start = timer()

        pipes_qs = self._get_pipe_and_asset_data()

        query_offset, query_limit = self._get_query_offset_limit(pipes_qs)

        for offset in range(query_offset, query_limit, self.config.batch_size):
            limit = offset + self.config.batch_size

            # print(offset, limit, "a")

            sliced_qs = list(pipes_qs[offset:limit])

            self.calc_pipe_point_relative_positions(sliced_qs)

            self.create_nk_graph()

        end = timer()
        print(end - start)

    def nk_to_graphml(self):
        """
        Export the network graph to a GraphML file.
        Writes the network graph to a specified GraphML file using the NetworkKit library.
        """
        nk.writeGraph(self.G, self.config.outputfile, nk.Format.GML)

    def _get_query_offset_limit(self, pipes_qs):
        """
        Calculate query offset and limit for batching.
        Determines the offset and limit values for querying the database in batches based on
        the total number of pipes and user-defined settings.
        Parameters:
            pipes_qs (QuerySet): QuerySet object containing pipe data.
        Returns:
            tuple: A tuple containing the query offset and limit values.
        """

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
        """
        Retrieve pipe and asset data from the database.
        Retrieves pipe mains and distribution mains data from the database and combines them
        into a single QuerySet.
        Returns:
            QuerySet: A QuerySet object containing pipe and asset data.
        """

        filters = {"dma_codes": self.config.dma_codes}

        pipe_qs: QuerySet = self.get_pipe_mains_data(filters)

        return pipe_qs

    def get_pipe_mains_data(self, filters={}) -> QuerySet:
        """
        Retrieve trunk mains data from the database.
        Uses the TrunkMainsController to query and retrieve trunk mains data from the database.
        Returns:
            QuerySet: A QuerySet object containing trunk mains data.
        """

        tm: PipeMainsController = PipeMainsController()
        return tm.get_pipe_point_relation_queryset(filters)
