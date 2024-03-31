import json
from multiprocessing import Pool
from collections import OrderedDict
from django.contrib.gis.geos import GEOSGeometry, LineString, Point
from django.db.models.query import QuerySet
from cwa_geod.config.settings import sqids
from cleanwater.core.utils import normalised_point_position_on_line
from cwa_geod.assets.models.trunk_main import TrunkMain
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

    def _map_relative_positions_calc(
        self, pipe_qs_object: TrunkMain
    ) -> tuple[dict, list]:
        # Convert the base pipe data from a queryset object to a dictionary
        base_pipe_data: dict = self._get_pipe_data(pipe_qs_object)

        # Convert all the data from intersecting pipes and point assets into
        # a list of dictionaries
        junctions_and_assets: list = self._combine_all_asset_data(pipe_qs_object)

        # Get the intersection points of all intersecting pipes (pipe junctions)
        # and the intersection points of all point assets. Then order them
        # relative to the start point of the line. The junction_and_asset_positions
        # returned matched the actual physical order that occurs geospatially
        junctions_and_assets_with_positions = self._get_connections_points_on_pipe(
            pipe_qs_object.geometry,
            pipe_qs_object.start_point_geom,
            junctions_and_assets,
        )

        self._set_node_properties(base_pipe_data, junctions_and_assets_with_positions)

        return base_pipe_data, junctions_and_assets_normalised

    def _get_pipe_data(self, qs_object) -> dict:

        pipe_data: dict = {}

        pipe_data["id"] = qs_object.pk
        pipe_data["gid"] = qs_object.gid
        pipe_data["asset_name"] = qs_object.asset_name
        pipe_data["pipe_length"] = qs_object.pipe_length
        pipe_data["wkt"] = qs_object.wkt
        pipe_data["dma_ids"] = qs_object.dma_ids
        pipe_data["dma_codes"] = qs_object.dma_codes
        pipe_data["dma_names"] = qs_object.dma_names
        pipe_data["utility_name"] = self._get_utility(qs_object)
        pipe_data["geometry"] = qs_object.geometry
        pipe_data["start_point_geom"] = qs_object.start_point_geom
        pipe_data["end_point_geom"] = qs_object.end_point_geom
        pipe_data["line_start_intersection_gids"] = list(
            set(qs_object.line_start_intersection_gids)
        )
        pipe_data["line_end_intersection_gids"] = list(
            set(qs_object.line_end_intersection_gids)
        )
        # pipe_data["start_geom_latlong"] = qs_object.start_geom_latlong
        # pipe_data["end_geom_latlong"] = qs_object.end_geom_latlong

        # TODO: maybe convert pipe data to simplenamespace
        # SimpleNamespace

        return pipe_data

    def _combine_all_asset_data(self, pipe_qs_object: TrunkMain) -> list:
        return (
            pipe_qs_object.trunkmain_junctions
            + pipe_qs_object.distmain_junctions
            + pipe_qs_object.chamber_data
            + pipe_qs_object.operational_site_data
            + pipe_qs_object.network_meter_data
            + pipe_qs_object.logger_data
            + pipe_qs_object.hydrant_data
            + pipe_qs_object.pressure_fitting_data
            + pipe_qs_object.pressure_valve_data
            + pipe_qs_object.network_opt_valve
        )

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

    def _map_get_normalised_positions(
        self, base_pipe_geom, start_point_geom, junction_or_asset: dict
    ) -> list:
        intersection_geom = self._get_intersecting_geometry(
            base_pipe_geom, junction_or_asset
        )

        if intersection_geom.geom_type == "Point":
            intersection_params = normalised_point_position_on_line(
                base_pipe_geom, start_point_geom, intersection_geom
            )
            data = [
                {
                    **junction_or_asset,
                    "intersection_point_geometry": intersection_geom,
                    "position": intersection_params[0],
                    # distance returned is based on srid and should be in meters.
                    # Convert to cm and round.
                    "distance_from_pipe_start": round(intersection_params[1] * 100),
                }
            ]

        elif intersection_geom.geom_type == "MultiPoint":
            data = []
            for coords in intersection_geom.coords:
                intersection_params = normalised_point_position_on_line(
                    base_pipe_geom,
                    start_point_geom,
                    Point(coords, srid=self.config.srid),
                )

                data.append(
                    {
                        **junction_or_asset,
                        "intersection_point_geometry": intersection_geom,
                        "position": intersection_params[0],
                        "distance_from_pipe_start": intersection_params[1],
                    }
                )

        else:
            raise Exception(
                "Invalid geometry types for intersection. Allowed types are point and multipoint"
            )

        return data

    def _get_connections_points_on_pipe(
        self, base_pipe_geom: LineString, start_point_geom, junction_and_assets: list
    ) -> list:
        junctions_and_assets_intersections = []

        # Not inefficient to use for loop with append here as the number of intersecting
        # junctions_and_assets for any given base pipe is not large
        for ja in junction_and_assets:
            intersections = self._map_get_normalised_positions(
                base_pipe_geom, start_point_geom, ja
            )
            junctions_and_assets_intersections += intersections

        return junctions_and_assets_intersections

    def _set_node_properties(self, base_pipe_data, junctions_and_assets_intersections):

        pipes_only = []
        point_assets_only = []
        for ja in junctions_and_assets_intersections:
            if ja["asset_name"] in PIPE_ASSETS__NAMES:
                pipes_only.append((ja["gid"], ja["distance_from_pipe_start"]))
            else:
                point_assets_only.append((ja["gid"], ja["distance_from_pipe_start"]))

        all_intersecting_pipes = [pipe[0] for pipe in pipes_only]

        pipes_intersecting_at_base_pipe_start_point = [
            gid
            for gid in base_pipe_data["line_start_intersection_gids"]
            if gid != base_pipe_data["gid"]
        ]

        pipes_intersecting_at_base_pipe_end_point = [
            gid
            for gid in base_pipe_data["line_end_intersection_gids"]
            if gid != base_pipe_data["gid"]
        ]

        non_termini_intersecting_pipes = list(
            set(all_intersecting_pipes).difference(
                pipes_intersecting_at_base_pipe_start_point
                + pipes_intersecting_at_base_pipe_end_point
            )
        )

        pipes_only.append((999999, 50))
        pipes_only.append((77777, 73))
        pipes_only.append((88888888, 73))
        pipes_only.append((333333, 50))
        non_termini_intersecting_pipes.append(88888888)
        non_termini_intersecting_pipes.append(333333)
        non_termini_intersecting_pipes.append(999999)

        pipes_only.append((111111, 73))
        non_termini_intersecting_pipes.append(77777)
        non_termini_intersecting_pipes.append(111111)

        pipes_only.append((222222, 80))
        non_termini_intersecting_pipes.append(222222)

        pipes_only.append((222222, 35))

        start_node_distance_cm = 0
        end_node_distance_cm = round(base_pipe_data["pipe_length"].cm)

        nodes_unordered = [
            {
                "gids": pipes_intersecting_at_base_pipe_start_point,
                "distance_from_pipe_start_cm": start_node_distance_cm,
                # "dmas": self.build_dma_data_as_json(dma_codes, dma_names),
                # "utility": utility_name
            },
            {
                "gids": pipes_intersecting_at_base_pipe_end_point,
                "distance_from_pipe_start_cm": round(
                    base_pipe_data["pipe_length"].cm
                ),  # need to be an int for sqid compatible hashing
            },
        ]

        yellow = {}
        for pipe_gid, distance_from_start_cm in pipes_only:
            # distance_from_start_cm must be an int for sqid
            # compatible hashing
            if pipe_gid in non_termini_intersecting_pipes:
                if distance_from_start_cm not in yellow.keys():
                    yellow[distance_from_start_cm] = {}
                    yellow[distance_from_start_cm]["gids"] = sorted(
                        [base_pipe_data["gid"], pipe_gid]
                    )
                    yellow[distance_from_start_cm][
                        "distance_from_pipe_start_cm"
                    ] = distance_from_start_cm
                else:
                    yellow[distance_from_start_cm]["gids"].append(pipe_gid)
                    yellow[distance_from_start_cm]["gids"] = sorted(
                        yellow[distance_from_start_cm]["gids"]
                    )

        point_assets_unordered = []
        for asset_gid, distance_from_start_cm in point_assets_only:
            point_assets_unordered.append(
                {
                    "gid": asset_gid,
                    "distance_from_pipe_start_cm": distance_from_start_cm,
                }
            )

        #                     "node_id": sqids.encode(
        #     [
        #         end_node_distance_cm,
        #         *pipes_intersecting_at_base_pipe_end_point,
        #     ]
        # ),

        nodes_unordered = (
            nodes_unordered + list(yellow.values()) + point_assets_unordered
        )
        import pdb

        pdb.set_trace()

        sorted(
            nodes_unordered,
            key=lambda x: x["distance_from_pipe_start_cm"],
        )
        import pdb

        pdb.set_trace()

    @staticmethod
    def _get_node_type(asset_name: str) -> str:
        if asset_name in PIPE_ASSETS__NAMES:
            return PIPE_END__NAME

        return POINT_ASSET__NAME

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

    @staticmethod
    def build_dma_data_as_json(dma_codes, dma_names):
        dma_data = [
            {"code": dma_code, "name": dma_name}
            for dma_code, dma_name in zip(dma_codes, dma_names)
        ]

        return json.dumps(dma_data)
