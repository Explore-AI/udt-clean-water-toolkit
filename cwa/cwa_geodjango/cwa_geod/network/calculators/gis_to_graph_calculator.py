import json
import bisect
from multiprocessing import Pool
from django.contrib.gis.geos import GEOSGeometry, LineString, Point
from django.db.models.query import QuerySet
from cwa_geod.config.settings import sqids
from cleanwater.core.utils import normalised_point_position_on_line
from cwa_geod.assets.models.trunk_main import TrunkMain
from cwa_geod.core.constants import (
    PIPE_END__NAME,
    PIPE_JUNCTION__NAME,
    POINT_ASSET__NAME,
    GEOS_LINESTRING_TYPES,
    GEOS_POINT_TYPES,
)


class GisToGraphCalculator:
    def __init__(self, config):
        self.config = config
        self.all_base_pipes = []
        self.all_nodes_ordered = []

    def calc_pipe_point_relative_positions(self, pipes_qs: list) -> None:
        self.all_base_pipes, self.all_nodes_ordered = list(
            zip(
                *map(
                    self._map_relative_positions_calc,
                    pipes_qs,
                )
            )
        )

    def calc_pipe_point_relative_positions_parallel(self, pipes_qs: list) -> None:
        with Pool(processes=self.config.processor_count) as p:
            self.all_base_pipes, self.all_nodes_ordered = zip(
                *p.imap_unordered(
                    self._map_relative_positions_calc,
                    pipes_qs,
                    self.config.chunk_size,
                )
            )

    def _map_relative_positions_calc(
        self, pipe_qs_object: TrunkMain
    ) -> tuple[dict, list]:
        # Convert the base pipe data from a queryset object to a dictionary
        base_pipe: dict = self._get_base_pipe_data(pipe_qs_object)

        # Convert all the data from intersecting pipes into
        # a list of dictionaries
        pipe_junctions: list = self._combine_all_pipe_junnctions(pipe_qs_object)

        # Convert all the data from point assets into a list of dictionaries
        point_assets: list = self._combine_all_point_assets(pipe_qs_object)

        # Get the intersection points of all intersecting pipes (pipe junctions)
        junctions_with_positions = self._get_connections_points_on_pipe(
            base_pipe,
            pipe_junctions,
        )

        # Get the intersection points of all point assets
        point_assets_with_positions = self._get_connections_points_on_pipe(
            base_pipe,
            point_assets,
        )

        # Set node properties and order them relative to the start point
        # of the line. The junction and asset nodes returned matches the
        # actual physical order that occurs geospatially
        nodes_ordered = self._set_node_properties(
            base_pipe, junctions_with_positions, point_assets_with_positions
        )

        #        self._set_relationship_properties(base_pipe, nodes_ordered)

        return base_pipe, nodes_ordered

    def _get_base_pipe_data(self, qs_object) -> dict:

        base_pipe: dict = {}

        base_pipe["id"] = qs_object.pk
        base_pipe["gid"] = qs_object.gid
        base_pipe["asset_name"] = qs_object.asset_name
        base_pipe["pipe_length"] = qs_object.pipe_length
        base_pipe["wkt"] = qs_object.wkt
        base_pipe["dma_ids"] = qs_object.dma_ids
        base_pipe["dma_codes"] = qs_object.dma_codes
        base_pipe["dma_names"] = qs_object.dma_names
        base_pipe["dmas"] = self.build_dma_data_as_json(
            base_pipe["dma_codes"], base_pipe["dma_names"]
        )
        base_pipe["utility_name"] = self._get_utility(qs_object)
        base_pipe["geometry"] = qs_object.geometry
        base_pipe["start_point_geom"] = qs_object.start_point_geom
        base_pipe["end_point_geom"] = qs_object.end_point_geom

        base_pipe["line_start_intersection_gids"] = (
            qs_object.line_start_intersection_gids
        )
        base_pipe["line_start_intersection_gids"].remove(qs_object.gid)

        base_pipe["line_end_intersection_gids"] = qs_object.line_end_intersection_gids
        base_pipe["line_end_intersection_gids"].remove(qs_object.gid)

        # base_pipe["start_geom_latlong"] = qs_object.start_geom_latlong
        # base_pipe["end_geom_latlong"] = qs_object.end_geom_latlong

        # TODO: maybe convert base_pipe to simplenamespace
        # SimpleNamespace

        return base_pipe

    def _combine_all_pipe_junnctions(self, pipe_qs_object: TrunkMain) -> list:
        return pipe_qs_object.trunkmain_junctions + pipe_qs_object.distmain_junctions

    def _combine_all_point_assets(self, pipe_qs_object: TrunkMain) -> list:
        return (
            pipe_qs_object.chamber_data
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
                    "distance_from_pipe_start_cm": round(intersection_params[1] * 100),
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
                        "distance_from_pipe_start_cm": intersection_params[1],
                    }
                )

        else:
            raise Exception(
                "Invalid geometry types for intersection. Allowed types are point and multipoint"
            )

        return data

    def _get_connections_points_on_pipe(
        self, base_pipe: dict, intersected_objects: list
    ) -> list:

        object_intersections = []
        # Not inefficient to use for loop with append here as the number
        # of intersecting junctions_and_assets for any given base pipe is not large
        for ja in intersected_objects:
            intersection = self._map_get_normalised_positions(
                base_pipe["geometry"], base_pipe["start_point_geom"], ja
            )
            object_intersections += intersection

        return object_intersections

    @staticmethod
    def _get_non_termini_intersecting_pipes(base_pipe_data, junctions_with_positions):

        termini_intersecting_pipe_gids = (
            base_pipe_data["line_start_intersection_gids"]
            + base_pipe_data["line_end_intersection_gids"]
        )

        non_termini_intersecting_pipes = [
            pipe
            for pipe in junctions_with_positions
            if pipe["gid"] not in termini_intersecting_pipe_gids
        ]

        # non_termini_intersecting_pipes.append(
        #     {"gid": 88888888, "distance_from_pipe_start_cm": 73}
        # )
        # non_termini_intersecting_pipes.append(
        #     {"gid": 333333, "distance_from_pipe_start_cm": 50}
        # )
        # non_termini_intersecting_pipes.append(
        #     {"gid": 999999, "distance_from_pipe_start_cm": 50}
        # )
        # non_termini_intersecting_pipes.append(
        #     {"gid": 77777, "distance_from_pipe_start_cm": 73}
        # )
        # non_termini_intersecting_pipes.append(
        #     {"gid": 111111, "distance_from_pipe_start_cm": 73}
        # )
        # non_termini_intersecting_pipes.append(
        #     {"gid": 222222, "distance_from_pipe_start_cm": 35}
        # )

        return non_termini_intersecting_pipes

    def _set_terminal_nodes(self, base_pipe):

        start_node_distance_cm = 0
        # round to int to make distance comparisons more robust
        end_node_distance_cm = round(base_pipe["pipe_length"].cm)

        line_start_intersection_gids = base_pipe["line_start_intersection_gids"]
        line_end_intersection_gids = base_pipe["line_end_intersection_gids"]

        start_node_gids = sorted([base_pipe["gid"], *line_start_intersection_gids])
        end_node_gids = sorted([base_pipe["gid"], *line_end_intersection_gids])

        if not line_start_intersection_gids:
            start_node_type = PIPE_END__NAME
        else:
            start_node_type = PIPE_JUNCTION__NAME

        if not line_end_intersection_gids:
            end_node_type = PIPE_END__NAME
        else:
            end_node_type = PIPE_JUNCTION__NAME

        nodes_ordered = [
            {
                "gids": start_node_gids,
                "node_type": start_node_type,
                "distance_from_pipe_start_cm": start_node_distance_cm,
                "dmas": base_pipe["dma_codes"],
                "intersection_point_geometry": base_pipe["start_point_geom"],
                "node_id": self._encode_node_id(
                    base_pipe["start_point_geom"],
                    start_node_gids,
                ),
                **base_pipe,
            },
            {
                "gids": end_node_gids,
                "node_type": end_node_type,
                "distance_from_pipe_start_cm": end_node_distance_cm,
                "dmas": base_pipe["dma_codes"],
                "intersection_point_geometry": base_pipe["end_point_geom"],
                "node_id": self._encode_node_id(
                    base_pipe["end_point_geom"],
                    end_node_gids,
                ),
                **base_pipe,
            },
        ]

        return nodes_ordered

    def _set_non_terminal_nodes(
        self, base_pipe, nodes_ordered, non_termini_intersecting_pipes
    ):

        distances = [x["distance_from_pipe_start_cm"] for x in nodes_ordered]

        for pipe in non_termini_intersecting_pipes:

            pipe_gid = pipe["gid"]
            # distance_from_start_cm must be an
            # int for sqid compatible hashing
            distance_from_pipe_start_cm = pipe["distance_from_pipe_start_cm"]

            if distance_from_pipe_start_cm not in distances:
                gids = sorted([pipe_gid, base_pipe["gid"]])

                position_index = bisect.bisect_right(
                    nodes_ordered,
                    distance_from_pipe_start_cm,
                    key=lambda x: x["distance_from_pipe_start_cm"],
                )

                nodes_ordered.insert(
                    # TODO: node_id may not be unique if different types of pipes have the same gid. FIX by defining a pipe_code
                    position_index,
                    {
                        "gids": gids,
                        "node_type": PIPE_JUNCTION__NAME,
                        "distance_from_pipe_start_cm": distance_from_pipe_start_cm,
                        "dmas": base_pipe["dmas"],
                        "intersection_point_geometry": pipe[
                            "intersection_point_geometry"
                        ],
                        "node_id": self._encode_node_id(
                            pipe["intersection_point_geometry"],
                            gids,
                        ),
                        **base_pipe,
                    },
                )

                distances.append(distance_from_pipe_start_cm)
            else:
                nodes_ordered[position_index]["gids"].append(pipe_gid)
                nodes_ordered[position_index]["gids"] = sorted(
                    nodes_ordered[position_index]["gids"]
                )

                # TODO: This is inefficient. Should hash only once all gids are known.
                nodes_ordered[position_index]["node_id"] = self._encode_node_id(
                    base_pipe["start_point_geom"],
                    [base_pipe["gid"], pipe_gid],
                )

        return nodes_ordered

    def _set_point_asset_properties(
        self, base_pipe, nodes_ordered, point_assets_with_positions
    ):
        for asset in point_assets_with_positions:
            # TODO: node_id may not be unique between assets. FIX by defining an asset_code
            bisect.insort(
                nodes_ordered,
                {
                    "distance_from_pipe_start_cm": asset["distance_from_pipe_start_cm"],
                    "node_type": POINT_ASSET__NAME,
                    "dmas": base_pipe["dma_codes"],
                    "node_id": self._encode_node_id(
                        asset["intersection_point_geometry"],
                        sorted([base_pipe["gid"], asset["gid"]]),
                    ),
                    **asset,
                },
                key=lambda x: x["distance_from_pipe_start_cm"],
            )

        return nodes_ordered

    def _set_node_properties(
        self, base_pipe, junctions_with_positions, point_assets_with_positions
    ):

        non_termini_intersecting_pipes = self._get_non_termini_intersecting_pipes(
            base_pipe, junctions_with_positions
        )

        nodes_ordered = self._set_terminal_nodes(base_pipe)

        nodes_ordered = self._set_non_terminal_nodes(
            base_pipe, nodes_ordered, non_termini_intersecting_pipes
        )

        nodes_ordered = self._set_point_asset_properties(
            base_pipe, nodes_ordered, point_assets_with_positions
        )

        return nodes_ordered

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

    @staticmethod
    def _encode_node_id(point, gids):
        """
        Round and cast Point geometry coordinates to str to remove '.'
        then return back to int to make make coords sqid compatible.

        Note these are not coordinates but int representations of the
        coordinates to ensure a unique node_id.
        """

        coord1_repr = int(str(round(point.coords[0], 3)).replace(".", ""))
        coord2_repr = int(str(round(point.coords[0], 3)).replace(".", ""))
        return sqids.encode(
            [
                coord1_repr,
                coord2_repr,
                *gids,
            ]
        )
