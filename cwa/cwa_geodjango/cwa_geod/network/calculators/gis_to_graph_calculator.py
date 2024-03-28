import bisect
from multiprocessing import Pool
from collections import OrderedDict
from networkx import Graph
from django.contrib.gis.geos import GEOSGeometry, LineString, Point
from django.db.models.query import QuerySet
from cleanwater.controllers.network_controller import NetworkController
from cleanwater.core.utils import normalised_point_position_on_line
from cwa_geod.assets.controllers import TrunkMainsController
from cwa_geod.assets.models.trunk_main import TrunkMain
from cwa_geod.assets.controllers import DistributionMainsController
from cwa_geod.core.constants import (
    PIPE_END__NAME,
    POINT_ASSET__NAME,
    PIPE_ASSETS__NAMES,
    GEOS_LINESTRING_TYPES,
    GEOS_POINT_TYPES,
)


class GisToGraphCalculator(NetworkController):
    def __init__(self, config):
        self.config = config
        super().__init__(srid=config.srid)

    def _create_pipe_single_intersection_data(
        self,
        asset,
        normalised_positions,
        base_pipe_geom,
        start_point_geom,
        intersection_geom,
    ):
        normalised_position_on_pipe: float = normalised_point_position_on_line(
            base_pipe_geom,
            start_point_geom,
            intersection_geom,
            srid=self.config.srid,
        )

        # intersection_geom_latlong = intersection_geom.transform("WGS84", clone=True)

        bisect.insort(
            normalised_positions,
            {
                "position": normalised_position_on_pipe,
                "data": asset,
                "intersection_point_geometry": intersection_geom,
                # "intersection_point_geom_latlong": intersection_geom_latlong,
            },
            key=lambda x: x["position"],
        )

        return normalised_positions

    def _create_pipe_multiple_intersection_data(
        self,
        asset,
        normalised_positions,
        base_pipe_geom,
        start_point_geom,
        intersection_geom,
    ):
        # handle multiple intersections
        for coords in intersection_geom.coords:
            normalised_positions = self._create_pipe_single_intersection_data(
                asset,
                normalised_positions,
                base_pipe_geom,
                start_point_geom,
                Point(coords, srid=self.srid),
            )

        return normalised_positions

    def _get_connections_points_on_pipe(
        self, base_pipe_geom: LineString, start_point_geom, asset_data: list
    ) -> list:
        normalised_positions: list = []

        for asset in asset_data:
            # Geom of the intersecting pipe or asset
            pipe_or_asset_geom = GEOSGeometry(asset["wkt"], srid=self.config.srid)

            # if pipe_or_asset_geom is a line then get the intersection point of the two lines
            if pipe_or_asset_geom.geom_typeid in GEOS_LINESTRING_TYPES:
                # __intersection__ may return a single or multipoint object

                intersection_geom = base_pipe_geom.intersection(pipe_or_asset_geom)

            elif pipe_or_asset_geom.geom_typeid in GEOS_POINT_TYPES:
                intersection_geom = pipe_or_asset_geom
            else:
                raise Exception(
                    f"Invalid GEOS line string type. Allowed types are {(',').join(str(x) for x in GEOS_LINESTRING_TYPES+GEOS_POINT_TYPES)}"
                )

            if intersection_geom.geom_type == "Point":
                normalised_positions = self._create_pipe_single_intersection_data(
                    asset,
                    normalised_positions,
                    base_pipe_geom,
                    start_point_geom,
                    intersection_geom,
                )
            elif intersection_geom.geom_type == "MultiPoint":
                normalised_positions = self._create_pipe_multiple_intersection_data(
                    asset,
                    normalised_positions,
                    base_pipe_geom,
                    start_point_geom,
                    intersection_geom,
                )

        return normalised_positions

    def _get_pipe_data(self, qs_object: TrunkMain) -> dict:
        pipe_data: dict = {}

        pipe_data["id"] = qs_object.pk
        pipe_data["gid"] = qs_object.gid
        pipe_data["asset_name"] = qs_object.asset_name
        pipe_data["length"] = qs_object.length
        pipe_data["wkt"] = qs_object.wkt
        pipe_data["dma_ids"] = qs_object.dma_ids
        pipe_data["dma_codes"] = qs_object.dma_codes
        pipe_data["dma_names"] = qs_object.dma_names
        pipe_data["utility_name"] = self._get_utility(qs_object)
        pipe_data["geometry"] = qs_object.geometry
        pipe_data["start_point_geom"] = qs_object.start_point_geom
        pipe_data["end_point_geom"] = qs_object.end_point_geom
        # pipe_data["start_geom_latlong"] = qs_object.start_geom_latlong
        # pipe_data["end_geom_latlong"] = qs_object.end_geom_latlong

        return pipe_data

    def _combine_all_asset_data(self, pipe_qs_object: TrunkMain) -> list:
        return (
            pipe_qs_object.trunk_mains_data
            + pipe_qs_object.distribution_mains_data
            + pipe_qs_object.chamber_data
            + pipe_qs_object.operational_site_data
            + pipe_qs_object.network_meter_data
            + pipe_qs_object.logger_data
            + pipe_qs_object.hydrant_data
            + pipe_qs_object.pressure_fitting_data
            + pipe_qs_object.pressure_valve_data
        )

    def _set_node_properties(self, pipe_data, junction_and_assets):
        all_nodes_ordered = OrderedDict()

        all_nodes_ordered[0.0] = {**pipe_data}

        for i, ja in enumerate(junction_and_assets):
            if ja["data"]["asset_name"] in dict(PIPE_ASSETS__NAMES).keys():
                junction_and_assets[i]["junction_gids"] = sorted(
                    [pipe_data["gid"], ja["data"]["gid"]]
                )
        import pdb

        pdb.set_trace()
        return junction_and_assets

    def _map_relative_positions_calc(
        self, pipe_qs_object: TrunkMain
    ) -> tuple[dict, list]:
        # Convert the base pipe data from a queryset object to a dictionary
        pipe_data: dict = self._get_pipe_data(pipe_qs_object)

        # Convert all the data from intersecting pipes and point assets into
        # a list of dictionaries
        junction_and_assets: list = self._combine_all_asset_data(pipe_qs_object)

        # Get the intersection points of all intersecting pipes (pipe junctions)
        # and the intersection points of all point assets. Then order them
        # relative to the start point of the line. The junction_and_asset_positions
        # returned matched the actual physical order that occurs geospatially
        junction_and_assets: list = self._get_connections_points_on_pipe(
            pipe_qs_object.geometry,
            pipe_qs_object.start_point_geom,
            junction_and_assets,
        )

        self._set_node_properties(pipe_data, junction_and_assets)

        return pipe_data, junction_and_assets

    def calc_pipe_point_relative_positions(self, pipes_qs: list) -> None:
        self.all_pipe_data, self.all_asset_positions = list(
            zip(
                *map(
                    self._map_relative_positions_calc,
                    pipes_qs,
                )
            )
        )

    def calc_pipe_point_relative_positions_parallel(
        self, pipes_qs_values: list
    ) -> None:
        with Pool(processes=self.config.processor_count) as p:
            self.all_pipe_data, self.all_asset_positions = zip(
                *p.imap_unordered(
                    self._map_relative_positions_calc,
                    pipes_qs_values,
                    self.config.chunk_size,
                )
            )

    @staticmethod
    def _get_node_type(asset_name: str) -> str:
        if asset_name in dict(PIPE_ASSETS__NAMES).keys():
            return PIPE_END__NAME

        return POINT_ASSET__NAME

    def get_trunk_mains_data(self) -> QuerySet:
        tm: TrunkMainsController = TrunkMainsController()
        return tm.get_pipe_point_relation_queryset()

    def get_distribution_mains_data(self) -> QuerySet:
        dm: DistributionMainsController = DistributionMainsController()
        return dm.get_pipe_point_relation_queryset()

    # TODO: remove from here as it contains specific nx methods
    def create_trunk_mains_graph(self) -> Graph:
        tm: TrunkMainsController = TrunkMainsController()

        trunk_mains: QuerySet = tm.get_geometry_queryset()
        return self.create_pipes_network(trunk_mains)

    def get_srid(self):
        """Get the currently used global srid"""
        return self.config.srid

    @staticmethod
    def get_pipe_count(qs) -> QuerySet:
        """Get the number of pipes in the provided queryset.
        Will make a call to the db. Strictly speaking will
        return the count of any queryset.

        Params:
              qs (Queryset). A queryset (preferably a union of all the pipe data)

        Returns:
              int: The queryset count:
        """

        return qs.count()

    @staticmethod
    def _get_utility(qs_object):
        utilities = list(set(qs_object.utility_names))

        if len(utilities) > 1:
            raise Exception(
                f"{qs_object} is located in multiple utilities. It should only be wtihing one"
            )
        return utilities[0]
