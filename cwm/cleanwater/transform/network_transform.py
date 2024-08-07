from collections import OrderedDict
from ..relations import PipeAndAssets
from . import GisToNeo4j, GisToNx, GisToNk


class NetworkTransform(PipeAndAssets):

    def __init__(self):
        self.method = None
        self.pipe_asset = None
        self.point_assets = OrderedDict()
        self.filters = {}

    def initialise(self, method, **kwargs):

        if method == "gis2neo4j":
            self.method = method
            self.intialise_gis2neo4j(**kwargs)
        elif method == "gis2nx":
            self.method = method
            self.intialise_gis2nx(**kwargs)
        elif method == "gis2nk":
            self.method = method
            self.intialise_gis2nk(**kwargs)
        else:
            raise Exception(
                "A valid method must be provided. Allowed values are 'gis2neo4j' ..."
            )

    def run(self, **kwargs):

        if self.method == "gis2neo4j":
            srid = kwargs.pop("srid")
            sqids = kwargs.pop("sqids")
            self.run_gis2neo4j(srid, sqids, **kwargs)

        elif self.method == "gis2nx":
            srid = kwargs.pop("srid")
            sqids = kwargs.pop("sqids")
            self.run_gis2nx(srid, sqids, **kwargs)

        elif self.method == "gis2nk":
            srid = kwargs.pop("srid")
            sqids = kwargs.pop("sqids")
            self.run_gis2nk(srid, sqids, **kwargs)

    def intialise_gis2neo4j(self, **kwargs):

        self.pipe_asset = kwargs.get("pipe_asset")
        self.point_assets = kwargs.get("point_assets", OrderedDict())
        self.filters = kwargs.get("filters", {})

        if not (self.pipe_asset or self.point_assets):
            raise Exception(
                "If the 'gis2neo4j' method is chosen a 'pipe_asset' and 'point_assets' must be specified."
            )

    def intialise_gis2nx(self, **kwargs):
        self.pipe_asset = kwargs.get("pipe_asset")
        self.point_assets = kwargs.get("point_assets", OrderedDict())
        self.filters = kwargs.get("filters", {})

        if not (self.pipe_asset or self.point_assets):
            raise Exception(
                "If the 'gis2nx' method is chosen a 'pipe_asset' and 'point_assets' must be specified."
            )

    def intialise_gis2nk(self, **kwargs):
        self.pipe_asset = kwargs.get("pipe_asset")
        self.point_assets = kwargs.get("point_assets", OrderedDict())
        self.filters = kwargs.get("filters", {})

        if not (self.pipe_asset or self.point_assets):
            raise Exception(
                "If the 'gis2nk' method is chosen a 'pipe_asset' and 'point_assets' must be specified."
            )

    def run_gis2neo4j(self, srid, sqids, **kwargs):

        gis_framework = kwargs.get("gis_framework")
        initial_query_limit = kwargs.get("query_limit")
        initial_query_offset = kwargs.get("query_offset")
        batch_size = kwargs.get("batch_size", 1)
        parallel = kwargs.get("parallel", False)
        processor_count = kwargs.get("processor_count", 2)
        chunk_size = kwargs.get("chunk_size", 1)

        if gis_framework == "geodjango":

            pipes_qs, pipes_pks = self.get_pipe_and_asset_data()

            query_offset, query_limit = self.get_query_offset_limit(
                pipes_pks, initial_query_limit, initial_query_offset
            )

            gtn = GisToNeo4j(
                srid,
                sqids,
                point_asset_names=list(self.point_assets.keys()),
                processor_count=processor_count,
                chunk_size=chunk_size,
            )

            for offset in range(query_offset, query_limit, batch_size):

                start_pk = pipes_pks[offset]

                pipe_data = list(pipes_qs.filter(pk__gte=start_pk)[:batch_size])

                if parallel:
                    gtn.calc_pipe_point_relative_positions_parallel(pipe_data)
                else:
                    gtn.calc_pipe_point_relative_positions(pipe_data)

                gtn.create_neo4j_graph()

        else:
            raise Exception(
                "The specified 'gis_framework' is not supported. Allowed values are 'geodjango', 'geoalchemy"
            )

    def run_gis2nx(self, srid, sqids, **kwargs):

        gis_framework = kwargs.get("gis_framework")
        initial_query_limit = kwargs.get("query_limit")
        initial_query_offset = kwargs.get("query_offset")
        batch_size = kwargs.get("batch_size", 1)

        if gis_framework == "geodjango":

            pipes_qs, pipes_pks = self.get_pipe_and_asset_data()

            query_offset, query_limit = self.get_query_offset_limit(
                pipes_pks, initial_query_limit, initial_query_offset
            )

            gtn = GisToNx(
                srid,
                sqids,
                point_asset_names=list(self.point_assets.keys()),
            )

            for offset in range(query_offset, query_limit, batch_size):

                start_pk = pipes_pks[offset]

                pipe_data = list(pipes_qs.filter(pk__gte=start_pk)[:batch_size])

                gtn.calc_pipe_point_relative_positions(pipe_data)

                gtn.create_nx_graph()

        else:
            raise Exception(
                "The specified 'gis_framework' is not supported. Allowed values are 'geodjango', 'geoalchemy"
            )

    def run_gis2nk(self, srid, sqids, **kwargs):
        gis_framework = kwargs.get("gis_framework")
        initial_query_limit = kwargs.get("query_limit")
        initial_query_offset = kwargs.get("query_offset")
        batch_size = kwargs.get("batch_size", 1)
        outputfile = kwargs.get("outputfile")

        if gis_framework == "geodjango":

            pipes_qs, pipes_pks = self.get_pipe_and_asset_data()

            query_offset, query_limit = self.get_query_offset_limit(
                pipes_pks, initial_query_limit, initial_query_offset
            )

            gtn = GisToNk(
                srid,
                sqids,
                point_asset_names=list(self.point_assets.keys()),
            )

            for offset in range(query_offset, query_limit, batch_size):

                start_pk = pipes_pks[offset]

                pipe_data = list(pipes_qs.filter(pk__gte=start_pk)[:batch_size])

                gtn.calc_pipe_point_relative_positions(pipe_data)

                gtn.create_nk_graph()

                gtn.nk_to_graphml(outputfile)

        else:
            raise Exception(
                "The specified 'gis_framework' is not supported. Allowed values are 'geodjango', 'geoalchemy"
            )

    # This fn is a candidate to be abstracted out into the NetworkController
    def get_pipe_and_asset_data(self):

        pipes_qs = self.get_pipe_and_point_relations(
            self.pipe_asset, self.point_assets, self.filters
        )

        pipes_pks = self.get_pipe_mains_pks(self.pipe_asset, self.filters)

        return pipes_qs, pipes_pks

    def get_query_offset_limit(self, pipes_pks, query_limit, query_offset):

        pipe_count = len(pipes_pks)

        if not query_limit:
            query_limit = pipe_count
        elif query_offset + query_limit == pipe_count:
            query_limit = pipe_count
        else:
            query_limit = query_offset + query_limit

        if not query_offset:
            query_offset = 0
        else:
            query_offset = query_offset

        return query_offset, query_limit
