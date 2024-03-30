from bisect import insort
from functools import partial
from multiprocessing import Pool
from collections import OrderedDict
from networkx import Graph
from django.contrib.gis.geos import GEOSGeometry, LineString, Point
from django.db.models.query import QuerySet
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


class GisToGraphCalculator:
    def __init__(self, config):
        self.config = config

    def _get_intersecting_geometry(self, base_pipe_geom, asset):
        # Geom of the intersecting pipe or asset
        pipe_or_asset_geom = GEOSGeometry(asset["wkt"], srid=self.config.srid)

        # if pipe_or_asset_geom is a line then get the intersection point of the two lines
        if pipe_or_asset_geom.geom_typeid in GEOS_LINESTRING_TYPES:
            # __intersection__ may return a single or multipoint object
            return base_pipe_geom.intersection(pipe_or_asset_geom)

        # otherwise if it is a point asset then get the point asset intersection
        elif pipe_or_asset_geom.geom_typeid in GEOS_POINT_TYPES:
            return pipe_or_asset_geom

        else:
            raise Exception(
                f"Invalid GEOS line string type. Allowed types are {(',').join(str(x) for x in GEOS_LINESTRING_TYPES+GEOS_POINT_TYPES)}"
            )

    def _map_get_normalised_positions(self, base_pipe_geom, start_point_geom, asset):
        intersection_geom = self._get_intersecting_geometry(base_pipe_geom, asset)

        if intersection_geom.geom_type == "Point":
            intersection_params = normalised_point_position_on_line(
                base_pipe_geom,
                start_point_geom,
                intersection_geom,
                srid=self.config.srid,
            )
            data = [
                {
                    **asset,
                    "intersection_point_geometry": intersection_geom,
                    "position": intersection_params[0],
                    "distance_from_pipe_start": intersection_params[1],
                }
            ]

            return data

        elif intersection_geom.geom_type == "MultiPoint":
            data = []
            for coords in intersection_geom.coords:
                intersection_params = normalised_point_position_on_line(
                    base_pipe_geom,
                    start_point_geom,
                    Point(coords, srid=self.config.srid),
                    srid=self.config.srid,
                )

                data.append(
                    {
                        **asset,
                        "intersection_point_geometry": intersection_geom,
                        "position": intersection_params[0],
                        "distance_from_pipe_start": intersection_params[1],
                    }
                )

                return data

        else:
            raise Exception(
                "Invalid geometry types for intersection. Allowed types are point and multipoint"
            )

    def _get_connections_points_on_pipe(
        self, base_pipe_geom: LineString, start_point_geom, asset_data: list
    ) -> list:
        mapfunc = partial(
            self._map_get_normalised_positions, base_pipe_geom, start_point_geom
        )
        normalised_intersections = list(zip(*map(mapfunc, asset_data)))[0]

        return normalised_intersections

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
            + pipe_qs_object.network_opt_valve
        )

    def _set_node_properties(self, pipe_data, junctions_and_assets):
        # all_nodes_ordered = OrderedDict()

        # for i, ja in enumerate(junctions_and_assets):
        #     if ja["data"]["asset_name"] in dict(PIPE_ASSETS__NAMES).keys():
        #         print(i, "qqq")
        #         all_nodes_ordered[i] = {
        #             "junction_gids": sorted([pipe_data["gid"], ja["data"]["gid"]])
        #         }

        #         for j, junc in enumerate(junctions_and_assets):
        #             print(j, "rrrr")
        #             distance_from_pipe_start_1 = round(
        #                 ja["distance_from_pipe_start"], 1
        #             )  # TODO: could move the round earlier
        #             distance_from_pipe_start_2 = round(
        #                 junc["distance_from_pipe_start"], 1
        #             )

        #             if distance_from_pipe_start_1 == distance_from_pipe_start_2:
        #                 x = all_nodes_ordered[i]["junction_gids"]
        #                 x.append(junc["data"]["gid"])
        #                 all_nodes_ordered[i]["junction_gids"] = sorted(list(set(x)))

        def _filter_for_common_junction(asset_data, pipe):
            distance_from_pipe_start_1 = round(
                asset_data["distance_from_pipe_start"], 1
            )  # TODO: could move the round earlier
            distance_from_pipe_start_2 = round(pipe["distance_from_pipe_start"], 1)

            if distance_from_pipe_start_1 == distance_from_pipe_start_2:
                return False

            return True

        i = 0
        nodes_ordered = OrderedDict()
        pipes_only = [
            x for x in junctions_and_assets if x["asset_name"] in PIPE_ASSETS__NAMES
        ]

        while True:
            if i == len(junctions_and_assets):
                break

            asset_data = junctions_and_assets[i]

            # if intersection is a pipe add pipe gids of intersection
            if asset_data["asset_name"] in PIPE_ASSETS__NAMES:
                nodes_ordered[i] = {
                    "junction_gids": sorted([pipe_data["gid"], asset_data["gid"]]),
                    **asset_data,
                }

                x = list(
                    filter(
                        lambda pipe: _filter_for_common_junction(asset_data, pipe),
                        pipes_only,
                    )
                )

            else:
                nodes_ordered[i] = junctions_and_assets[i]

            i += 1

        return junctions_and_assets

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
        junctions_and_assets: list = self._get_connections_points_on_pipe(
            pipe_qs_object.geometry,
            pipe_qs_object.start_point_geom,
            junction_and_assets,
        )

        self._set_node_properties(pipe_data, junctions_and_assets)

        return pipe_data, junctions_and_assets

    def calc_pipe_point_relative_positions(self, pipes_qs: list) -> None:
        self.all_pipe_data, self.all_asset_positions = list(
            zip(
                *map(
                    self._map_relative_positions_calc,
                    pipes_qs,
                )
            )
        )
        import pdb

        pdb.set_trace()

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
        if asset_name in PIPE_ASSETS__NAMES:
            return PIPE_END__NAME

        return POINT_ASSET__NAME

    def get_trunk_mains_data(self) -> QuerySet:
        tm: TrunkMainsController = TrunkMainsController()
        return tm.get_pipe_point_relation_queryset()

    def get_distribution_mains_data(self) -> QuerySet:
        dm: DistributionMainsController = DistributionMainsController()
        return dm.get_pipe_point_relation_queryset()

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
