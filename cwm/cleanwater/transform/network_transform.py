from collections import OrderedDict
from ..relations import PipeAndAssets
from . import GisToGraph


class NetworkTransform(PipeAndAssets):

    def __init__(self):
        self.method = None
        self.pipe_asset = None
        self.point_assets = OrderedDict()
        self.filters = {}

    def initialise(self, method, **kwargs):

        if method == "gis2neo4j":
            self.intialise_gis2neo4j(**kwargs)
            self.method = method
        else:
            raise Exception(
                "A valid method must be provided. Allowed values are 'gis2neo4j' ..."
            )

    def run(self, **kwargs):

        if self.method == "gis2neo4j":
            srid = kwargs.pop("srid")
            sqids = kwargs.pop("sqids")
            self.run_gis2neo4j(srid, sqids, **kwargs)

    def intialise_gis2neo4j(self, **kwargs):

        self.pipe_asset = kwargs.get("pipe_asset")
        self.point_assets = kwargs.get("point_assets", OrderedDict())
        self.filters = kwargs.get("filters", {})

        if not (self.pipe_asset or self.point_assets):
            raise Exception(
                "If the 'gis2neo4j' method is chosen a 'pipe_asset' and 'point_assets' must be specified."
            )

    def run_gis2neo4j(self, srid, sqids, **kwargs):

        gis_framework = kwargs.get("gis_framework")

        if gis_framework == "geodjango":
            qs = self.get_pipe_and_point_relations(
                self.pipe_asset, self.point_assets, self.filters
            )

            gtg = GisToGraph(
                srid, sqids, point_asset_names=list(self.point_assets.keys())
            )

            gtg.calc_pipe_point_relative_positions(list(qs[:5]))
        else:
            raise Exception(
                "The specified 'gis_framework' is not supported. Allowed values are 'geodjango', 'geoalchemy"
            )
