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
    def __init__(
        self,
        srid,
        processor_count=None,
        chunk_size=None,
    ):
        self.srid = srid
        self.processor_count = processor_count
        self.chunk_size = chunk_size

        self.all_edges_by_pipe = []
        self.all_nodes_by_pipe = []

    def calc_pipe_point_relative_positions(self, pipes_qs: list) -> None:
        self.all_nodes_by_pipe, self.all_edges_by_pipe = list(
            zip(
                *map(
                    self._map_relative_positions_calc,
                    pipes_qs,
                )
            )
        )

    def calc_pipe_point_relative_positions_parallel(self, pipes_qs: list) -> None:
        with Pool(processes=self.processor_count) as p:
            self.all_nodes_by_pipe, self.all_edges_by_pipe = zip(
                *p.imap_unordered(
                    self._map_relative_positions_calc,
                    pipes_qs,
                    self.chunk_size,
                )
            )

    def _map_relative_positions_calc(self, pipe_qs_object: TrunkMain):

        # Convert the base pipe data from a queryset object to a dictionary
        base_pipe: dict = self._get_base_pipe_data(pipe_qs_object)

        # Convert all the data from intersecting pipes into
        # a list of dictionaries
        pipe_junctions: list = self._combine_all_pipe_junctions(pipe_qs_object)

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

        nodes_by_pipe = self._merge_nodes_on_position(nodes_ordered)

        edges_by_pipe = self._get_edges_by_pipe(base_pipe, nodes_by_pipe)

        return nodes_by_pipe, edges_by_pipe

    def _get_edges_by_pipe(self, base_pipe, nodes_by_pipe):
        edges_by_pipe = []

        from_node = nodes_by_pipe[0]
        for to_node in nodes_by_pipe[1:]:
            edges_by_pipe.append(
                {
                    "from_node_key": from_node["node_key"],
                    "to_node_key": to_node["node_key"],
                    "gid": base_pipe["gid"],
                    "asset_name": base_pipe["asset_name"],
                    "asset_label": base_pipe["asset_label"],
                    "dmas": base_pipe["dmas"],
                }
            )
            from_node = to_node

        return edges_by_pipe

    def _merge_nodes_on_position(self, nodes_ordered):
        consolidated_nodes = [[nodes_ordered[0]]]

        prev_distance = round(nodes_ordered[0]["distance_from_pipe_start_cm"])
        for node in nodes_ordered[1:]:
            current_distance = round(node["distance_from_pipe_start_cm"])

            if current_distance == prev_distance:
                consolidated_nodes[-1].append(node)
            else:
                consolidated_nodes.append([node])

            prev_distance = current_distance

        merged_nodes = []
        for nodes in consolidated_nodes:

            merged_nodes.append(
                {
                    "utility": nodes[0]["utility_name"],
                    "coords_27700": [
                        float(nodes[0]["intersection_point_geometry"].x),
                        float(nodes[0]["intersection_point_geometry"].y),
                    ],
                    "node_key": self._encode_node_key(
                        nodes[0]["intersection_point_geometry"]
                    ),
                    "dmas": nodes[0]["dmas"],
                    "node_types": [],
                    "node_labels": ["PointNode"],
                }
            )

            for node in nodes:
                if node["node_type"] == PIPE_JUNCTION__NAME:
                    merged_nodes[-1]["node_types"].append(PIPE_JUNCTION__NAME)
                    merged_nodes[-1]["node_labels"].append("PipeJunction")
                    try:
                        merged_nodes[-1]["pipe_gids"].extend(node["pipe_gids"])
                    except KeyError:
                        merged_nodes[-1]["pipe_gids"] = node["pipe_gids"]
                elif node["node_type"] == PIPE_END__NAME:
                    merged_nodes[-1]["node_types"].append(PIPE_END__NAME)
                    merged_nodes[-1]["node_labels"].append("PipeEnd")
                    try:
                        merged_nodes[-1]["pipe_gid"].extend(node["gid"])
                    except KeyError:
                        merged_nodes[-1]["pipe_gid"] = node["gid"]
                elif node["node_type"] == POINT_ASSET__NAME:
                    merged_nodes[-1]["node_types"].append(POINT_ASSET__NAME)

                    subtype = node.get("subtype")
                    if subtype:
                        merged_nodes[-1]["subtype"] = subtype

                    acoustic_logger = node.get("acoustic_logger")
                    if acoustic_logger:
                        merged_nodes[-1]["acoustic_logger"] = acoustic_logger

                    if "PointAsset" not in merged_nodes[-1]["node_labels"]:
                        merged_nodes[-1]["node_labels"].append("PointAsset")
                    merged_nodes[-1]["node_labels"].append(node["asset_label"])

                    try:
                        merged_nodes[-1]["point_asset_names"].append(node["asset_name"])
                        merged_nodes[-1]["point_asset_gids"].append(node["gid"])
                        merged_nodes[-1]["point_assets_with_gids"][
                            f"{node['asset_name']}_gid"
                        ] = node["gid"]

                    except KeyError:
                        merged_nodes[-1]["point_asset_names"] = [node["asset_name"]]
                        merged_nodes[-1]["point_asset_gids"] = [node["gid"]]
                        merged_nodes[-1]["point_assets_with_gids"] = {
                            f"{node['asset_name']}_gid": node["gid"]
                        }

                # remove duplicates and sort node_types
                merged_nodes[-1]["node_types"] = sorted(
                    list(set((merged_nodes[-1]["node_types"])))
                )

        return merged_nodes

    def _get_base_pipe_data(self, qs_object) -> dict:
        base_pipe: dict = {}

        base_pipe["id"] = qs_object.pk
        base_pipe["gid"] = qs_object.gid
        base_pipe["asset_name"] = qs_object.asset_name
        base_pipe["asset_label"] = qs_object.asset_label
        base_pipe["pipe_length"] = qs_object.pipe_length
        base_pipe["wkt"] = qs_object.wkt
        base_pipe["dma_ids"] = qs_object.dma_ids
        base_pipe["dma_codes"] = qs_object.dma_codes
        base_pipe["dma_names"] = qs_object.dma_names
        base_pipe["dmas"] = self.build_dma_data_as_json(
            base_pipe["dma_codes"], base_pipe["dma_names"]
        )

        base_pipe["utilities"] = qs_object.utility_names
        base_pipe["geometry"] = qs_object.geometry
        base_pipe["start_point_geom"] = qs_object.start_point_geom
        base_pipe["end_point_geom"] = qs_object.end_point_geom

        base_pipe["line_start_intersection_gids"] = []
        base_pipe["line_start_intersection_ids"] = []
        for line in qs_object.line_start_intersections:
            base_pipe["line_start_intersection_gids"].extend(line["gids"])
            base_pipe["line_start_intersection_ids"].extend(line["ids"])

        base_pipe["line_start_intersection_gids"].remove(qs_object.gid)
        base_pipe["line_start_intersection_ids"].remove(qs_object.id)

        base_pipe["line_end_intersection_gids"] = []
        base_pipe["line_end_intersection_ids"] = []
        for line in qs_object.line_end_intersections:
            base_pipe["line_end_intersection_gids"].extend(line["gids"])
            base_pipe["line_end_intersection_ids"].extend(line["ids"])

        base_pipe["line_end_intersection_gids"].remove(qs_object.gid)
        base_pipe["line_end_intersection_ids"].remove(qs_object.id)

        # base_pipe["start_geom_latlong"] = qs_object.start_geom_latlong
        # base_pipe["end_geom_latlong"] = qs_object.end_geom_latlong

        # TODO: maybe convert base_pipe to simplenamespace
        # SimpleNamespace

        return base_pipe

    def _combine_all_pipe_junctions(self, pipe_qs_object: TrunkMain) -> list:
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

    @staticmethod
    def _get_intersecting_geometry(base_pipe_geom, wkt, srid):

        # Geom of the intersecting pipe or asset
        pipe_or_asset_geom = GEOSGeometry(wkt, srid)

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
        self, base_pipe_geom, junction_or_asset: dict
    ) -> list:

        intersection_geom = self._get_intersecting_geometry(
            base_pipe_geom, junction_or_asset["wkt"], self.srid
        )

        # if not intersection_geom_4326.coords:
        #     intersection_geom_4326 = intersection_geom.transform(4326, clone=True)

        if intersection_geom.geom_type == "Point":
            intersection_params = normalised_point_position_on_line(
                base_pipe_geom, intersection_geom.coords
            )
            data = [
                {
                    **junction_or_asset,
                    "intersection_point_geometry": intersection_geom,
                    # distance returned is based on srid and should be in meters.
                    # Convert to cm and round.
                    "distance_from_pipe_start_cm": round(intersection_params[0] * 100),
                    "normalised_position": intersection_params[1],
                }
            ]

        elif intersection_geom.geom_type == "MultiPoint":
            data = []
            for coords in intersection_geom.coords:
                intersection_params = normalised_point_position_on_line(
                    base_pipe_geom,
                    coords,
                )

                data.append(
                    {
                        **junction_or_asset,
                        "intersection_point_geometry": intersection_geom,
                        # distance returned is based on srid and should be in meters.
                        # Convert to cm and round.
                        "distance_from_pipe_start_cm": round(
                            intersection_params[0] * 100
                        ),
                        "normalised_position": intersection_params[1],
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
            intersection = self._map_get_normalised_positions(base_pipe["geometry"], ja)
            object_intersections += intersection

        return object_intersections

    @staticmethod
    def _get_non_termini_intersecting_pipes(base_pipe, junctions_with_positions):
        termini_intersecting_pipe_gids = (
            base_pipe["line_start_intersection_gids"]
            + base_pipe["line_end_intersection_gids"]
        )

        non_termini_intersecting_pipes = [
            pipe
            for pipe in junctions_with_positions
            if pipe["gid"] not in termini_intersecting_pipe_gids
        ]

        # non_termini_intersecting_pipes.append(
        #     {
        #         "id": 1,
        #         "gid": 88888888,
        #         "distance_from_pipe_start_cm": 73,
        #         "intersection_point_geometry": base_pipe["start_point_geom"],
        #     }
        # )
        # non_termini_intersecting_pipes.append(
        #     {
        #         "id": 2,
        #         "gid": 333333,
        #         "distance_from_pipe_start_cm": 50,
        #         "intersection_point_geometry": base_pipe["start_point_geom"],
        #     }
        # )
        # non_termini_intersecting_pipes.append(
        #     {
        #         "id": 3,
        #         "gid": 999999,
        #         "distance_from_pipe_start_cm": 50,
        #         "intersection_point_geometry": base_pipe["start_point_geom"],
        #     }
        # )
        # non_termini_intersecting_pipes.append(
        #     {
        #         "id": 4,
        #         "gid": 77777,
        #         "distance_from_pipe_start_cm": 73,
        #         "intersection_point_geometry": base_pipe["start_point_geom"],
        #     }
        # )
        # non_termini_intersecting_pipes.append(
        #     {
        #         "id": 5,
        #         "gid": 111111,
        #         "distance_from_pipe_start_cm": 73,
        #         "intersection_point_geometry": base_pipe["start_point_geom"],
        #     }
        # )
        # non_termini_intersecting_pipes.append(
        #     {
        #         "id": 6,
        #         "gid": 222222,
        #         "distance_from_pipe_start_cm": 35,
        #         "intersection_point_geometry": base_pipe["start_point_geom"],
        #     }
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
                "pipe_gids": start_node_gids,
                "node_type": start_node_type,
                "distance_from_pipe_start_cm": start_node_distance_cm,
                "dmas": base_pipe["dma_codes"],
                "intersection_point_geometry": base_pipe["start_point_geom"],
                "utility_name": self._get_utility(base_pipe),
                **base_pipe,
            },
            {
                "pipe_gids": end_node_gids,
                "node_type": end_node_type,
                "distance_from_pipe_start_cm": end_node_distance_cm,
                "dmas": base_pipe["dma_codes"],
                "intersection_point_geometry": base_pipe["end_point_geom"],
                "utility_name": self._get_utility(base_pipe),
                **base_pipe,
            },
        ]

        return nodes_ordered

    def _set_non_terminal_nodes(
        self, base_pipe, nodes_ordered, non_termini_intersecting_pipes
    ):
        distances = [x["distance_from_pipe_start_cm"] for x in nodes_ordered]

        position_index = 0
        for pipe in non_termini_intersecting_pipes:
            pipe_gid = pipe["gid"]
            # distance_from_start_cm must be an
            # int for sqid compatible hashing
            distance_from_pipe_start_cm = pipe["distance_from_pipe_start_cm"]

            gids = sorted([pipe_gid, base_pipe["gid"]])
            if distance_from_pipe_start_cm not in distances:

                position_index = bisect.bisect_right(
                    nodes_ordered,
                    distance_from_pipe_start_cm,
                    key=lambda x: x["distance_from_pipe_start_cm"],
                )

                nodes_ordered.insert(
                    position_index,
                    {
                        "pipe_gids": gids,
                        "node_type": PIPE_JUNCTION__NAME,
                        "utility_name": self._get_utility(base_pipe),
                        "distance_from_pipe_start_cm": distance_from_pipe_start_cm,
                        "dmas": base_pipe["dmas"],
                        "intersection_point_geometry": pipe[
                            "intersection_point_geometry"
                        ],
                        **base_pipe,
                    },
                )

                distances.append(distance_from_pipe_start_cm)
            else:
                nodes_ordered[position_index]["pipe_gids"].append(pipe_gid)
                nodes_ordered[position_index]["pipe_gids"] = sorted(
                    nodes_ordered[position_index]["pipe_gids"]
                )

        return nodes_ordered

    def _set_point_asset_properties(
        self, base_pipe, nodes_ordered, point_assets_with_positions
    ):

        for asset in point_assets_with_positions:

            # TODO: node_key may not be unique between assets. FIX by defining an asset_code
            bisect.insort(
                nodes_ordered,
                {
                    "distance_from_pipe_start_cm": asset["distance_from_pipe_start_cm"],
                    "node_type": POINT_ASSET__NAME,
                    "dmas": base_pipe["dmas"],
                    "utility_name": self._get_utility(base_pipe),
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

        # self._calc_pipe_length_between_nodes(nodes_ordered)

        return nodes_ordered

    def get_srid(self):
        """Get the currently used global srid"""
        return self.srid

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
        utilities = list(set(qs_object["utilities"]))

        if len(utilities) > 1:
            raise Exception(
                f"{qs_object} is located in multiple utilities. It should only be within one"
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
    def _encode_node_key(point):
        """
        Round and cast Point geometry coordinates to str to remove '.'
        then return back to int to make make coords sqid compatible.

        Note these are not coordinates but int representations of the
        coordinates to ensure a unique node_key.
        """

        coord1_repr = int(str(round(point.coords[0], 3)).replace(".", ""))
        coord2_repr = int(str(round(point.coords[1], 3)).replace(".", ""))
        return sqids.encode(
            [
                coord1_repr,
                coord2_repr,
            ]
        )
