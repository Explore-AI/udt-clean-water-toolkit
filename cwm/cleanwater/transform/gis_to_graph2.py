import json
import bisect
from random import randint
from multiprocessing import Pool
from django.contrib.gis.geos import GEOSGeometry
from django.db.models.query import QuerySet
from shapely.ops import substring
from shapely import LineString, Point, line_locate_point
from ..core.utils import normalised_point_position_on_line
from ..core.constants import (
    PIPE_END__NAME,
    PIPE_JUNCTION__NAME,
    POINT_ASSET__NAME,
    GEOS_LINESTRING_TYPES,
    GEOS_POINT_TYPES,
    NETWORK_NODE__LABEL,
    PIPE_NODE__LABEL,
    PIPE_JUNCTION__LABEL,
    PIPE_END__LABEL,
    POINT_ASSET__LABEL,
)


def flatten_concatenation(matrix):
    flat_list = []
    for row in matrix:
        flat_list += row
    return flat_list


class GisToGraph2:
    def __init__(
        self, srid, sqids, processor_count=None, chunk_size=None, neoj4_point=False
    ):
        self.srid = srid
        self.sqids = sqids
        self.processor_count = processor_count
        self.chunk_size = chunk_size
        self.neoj4_point = neoj4_point

        self.all_pipe_edges_by_pipe = []
        self.all_pipe_nodes_by_pipe = []
        self.all_asset_nodes_by_pipe = []
        self.all_pipe_node_to_asset_node_edges = []
        self.dma_data = []
        self.utility_data = []
        self.network_node_labels = [
            NETWORK_NODE__LABEL,
            PIPE_NODE__LABEL,
            PIPE_JUNCTION__LABEL,
            PIPE_END__LABEL,
            POINT_ASSET__LABEL,
        ]  # List of network node labels with no duplicates
        self.network_edge_labels = []  # List of pipe edge labels with no duplicates

    def calc_pipe_point_relative_positions(self, pipes_qs: list) -> None:
        (
            self.all_pipe_nodes_by_pipe,
            self.all_pipe_edges_by_pipe,
            self.all_asset_nodes_by_pipe,
            self.all_pipe_node_to_asset_node_edges,
            self.dma_data,
            self.utility_data,
            all_asset_node_labels,
        ) = list(
            zip(
                *map(
                    self._map_relative_positions_calc,
                    pipes_qs,
                )
            )
        )

        self.network_node_labels.extend(
            list(set(flatten_concatenation(all_asset_node_labels)))
        )

    def calc_pipe_point_relative_positions_parallel(self, pipes_qs: list) -> None:
        with Pool(processes=self.processor_count) as p:
            (
                self.all_pipe_nodes_by_pipe,
                self.all_pipe_edges_by_pipe,
                self.all_asset_nodes_by_pipe,
                self.all_pipe_node_to_asset_node_edges,
                self.dma_data,
                self.utility_data,
                all_asset_node_labels,
            ) = zip(
                *p.imap_unordered(
                    self._map_relative_positions_calc,
                    pipes_qs,
                    self.chunk_size,
                )
            )

        self.network_node_labels.extend(
            list(set(flatten_concatenation(all_asset_node_labels)))
        )

    def _map_relative_positions_calc(self, pipe_qs_object):

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
        # actual physical order that occurs geo-spatially
        nodes_ordered = self._set_node_properties(
            base_pipe, junctions_with_positions, point_assets_with_positions
        )

        (
            pipe_nodes_by_pipe,
            pipe_edges_by_pipe,
            asset_nodes_by_pipe,
            pipe_node_to_asset_node_edges,
            dma_data,
            utility_data,
            all_asset_node_labels,
        ) = self._set_nodes_and_edges(base_pipe, nodes_ordered)

        return (
            pipe_nodes_by_pipe,
            pipe_edges_by_pipe,
            asset_nodes_by_pipe,
            pipe_node_to_asset_node_edges,
            dma_data,
            utility_data,
            all_asset_node_labels,
        )

    def create_dma_data(self, node_data):

        dma_data = []
        for dma_code, dma_name in zip(node_data["dma_codes"], node_data["dma_names"]):
            dma_data.append(
                {
                    "code": dma_code,
                    "name": dma_name,
                    "to_node_key": node_data["node_key"],
                }
            )

        return dma_data

    def create_utility_data(self, node_data):

        return [
            {
                "name": node_data["utility"],
                "to_node_key": node_data["node_key"],
            }
        ]

    def _set_pipe_properties(self, node, pipe_node_data):

        pipe_node_data["node_key"] = self._encode_node_key(
            node["intersection_point_geometry"]
        )
        pipe_node_data["pipe_tags"] = node["pipe_tags"]

        return pipe_node_data

    def _merge_pipe_junction_node(self, node):
        pipe_node_data = {}

        pipe_node_data["node_labels"] = [PIPE_NODE__LABEL, PIPE_JUNCTION__LABEL]

        return self._set_pipe_properties(node, pipe_node_data)

    def _merge_pipe_end_node(self, node):
        pipe_node_data = {}
        pipe_node_data["node_labels"] = [PIPE_NODE__LABEL, PIPE_END__LABEL]

        return self._set_pipe_properties(node, pipe_node_data)

    def _handle_pipe_asset_node_labels(self, node):
        pipe_node_data = {}
        pipe_node_data["node_key"] = self._encode_node_key(
            node["intersection_point_geometry"]
        )

        pipe_node_data["node_labels"] = [PIPE_NODE__LABEL, PIPE_JUNCTION__LABEL]

        return pipe_node_data

    def _create_asset_node(self, node):
        asset_node_data = {}

        asset_node_data["node_labels"] = [
            NETWORK_NODE__LABEL,
            POINT_ASSET__LABEL,
            node["asset_label"],
        ]

        asset_node_data["node_key"] = self._encode_node_key(
            node["intersection_point_geometry"], extra_params=[randint(1, 100)]
        )

        asset_node_data["tag"] = node["tag"]

        # if node["asset_label"] not in self.network_node_labels:
        #     self.network_node_labels.append(node["asset_label"])

        subtype = node.get("subtype")
        if subtype:
            asset_node_data["subtype"] = subtype

        acoustic_logger = node.get("acoustic_logger")
        if acoustic_logger:
            asset_node_data["acoustic_logger"] = acoustic_logger

        return asset_node_data

    def _merge_point_asset_node(self, node):

        asset_node_data = self._create_asset_node(node)

        pipe_node_data = {}
        if node.get("is_non_termini_asset_node"):
            pipe_node_data = self._handle_pipe_asset_node_labels(node)

        return pipe_node_data, asset_node_data

    @staticmethod
    def _set_network_node_default_props(nodes) -> dict:

        return {
            "utility": nodes[0]["utility_name"],
            "coords_27700": [
                float(nodes[0]["intersection_point_geometry"].x),
                float(nodes[0]["intersection_point_geometry"].y),
            ],
            "dma_codes": nodes[0]["dma_codes"],
            "dma_names": nodes[0]["dma_names"],
            "dmas": nodes[0]["dmas"],
        }

    @staticmethod
    def _consolidate_nodes_on_position(nodes_ordered):
        """
        Combine nodes based on their distance from the
        start of the pipe.
        """
        consolidated_nodes = [[nodes_ordered[0]]]

        prev_distance = round(nodes_ordered[0]["distance_from_pipe_start_cm"])
        for node in nodes_ordered[1:]:
            current_distance = round(node["distance_from_pipe_start_cm"])

            if current_distance == prev_distance:
                consolidated_nodes[-1].append(node)
            else:
                consolidated_nodes.append([node])

            prev_distance = current_distance

        return consolidated_nodes

    def _reconfigure_nodes(self, node):

        asset_node_data = {}
        if node["node_type"] == PIPE_JUNCTION__NAME:
            pipe_node_data = self._merge_pipe_junction_node(node)
        elif node["node_type"] == PIPE_END__NAME:
            pipe_node_data = self._merge_pipe_end_node(node)
        elif node["node_type"] == POINT_ASSET__NAME:
            pipe_node_data, asset_node_data = self._merge_point_asset_node(node)
        else:
            raise Exception(f"Invalid node_type ({node['node_type']}) detected.")

        return pipe_node_data, asset_node_data

    @staticmethod
    def _merge_all_pipe_node_props(default_props, pipe_node_data):

        all_pipe_node_data = default_props | pipe_node_data

        try:
            all_pipe_node_data["node_labels"].append(NETWORK_NODE__LABEL)
        except KeyError:
            all_pipe_node_data["node_labels"] = [NETWORK_NODE__LABEL]

        return all_pipe_node_data

    @staticmethod
    def _merge_all_asset_node_props(default_props, asset_node_data):

        all_asset_node_data = {}
        if asset_node_data:
            all_asset_node_data = default_props | asset_node_data
            all_asset_node_data["node_labels"].append(NETWORK_NODE__LABEL)

        return all_asset_node_data

    def _create_pipe_asset_nodes(self, cnodes: list):

        default_props = self._set_network_node_default_props(cnodes)

        ### check if an asset node occurs at the
        ### non-termini of a pipe. We have do this
        ### to create a pipe-junction at this point.
        if (len(cnodes) == 1) and (cnodes[0]["node_type"] == POINT_ASSET__NAME):
            cnodes[0]["is_non_termini_asset_node"] = True

        all_pipe_node_data = {}
        all_asset_node_data = {}
        all_asset_node_labels = []
        all_dma_data = []
        all_utility_data = []
        for node in cnodes:

            pipe_node_data, asset_node_data = self._reconfigure_nodes(node)

            if pipe_node_data:
                all_pipe_node_data = self._merge_all_pipe_node_props(
                    default_props, pipe_node_data
                )
                utility_data = self.create_utility_data(all_pipe_node_data)
                dma_data = self.create_dma_data(all_pipe_node_data)
                all_utility_data.extend(utility_data)
                all_dma_data.extend(dma_data)

            if asset_node_data:
                all_asset_node_data = self._merge_all_asset_node_props(
                    default_props, asset_node_data
                )

                all_asset_node_labels.append(node["asset_label"])
                utility_data = self.create_utility_data(all_asset_node_data)
                dma_data = self.create_dma_data(all_asset_node_data)
                all_utility_data.extend(utility_data)
                all_dma_data.extend(dma_data)

        return (
            all_pipe_node_data,
            all_asset_node_data,
            all_dma_data,
            all_utility_data,
            all_asset_node_labels,
        )

    @staticmethod
    def _create_pipe_node_to_asset_node_edge(pipe_node, asset_nodes_for_pipe_node):

        edges = []

        from_node_key = pipe_node["node_key"]
        for asset_node in asset_nodes_for_pipe_node:
            to_node_key = asset_node["node_key"]
            edges.append(
                {
                    "from_node_key": from_node_key,
                    "to_node_key": to_node_key,
                    "edge_key": f"{from_node_key}-{to_node_key}",
                }
            )
        return edges

    def _set_network_node_and_edge_data(self, consolidated_nodes):
        """

        consolidated_nodes: list of nodes on a pipe ordered based on
        position from the start of the line. Each element is a list
        contains all pipe_junctions/assets or pipe_ends/assets at the
        same coordinates and this sublist has no order.

        cnodes: The pipe_junctions/assets or pipe_ends/assets at the
        same coordinates. There should only be one pipe_junction or pipe_end node.
        There can be any number of asset nodes. Has no particular order.

        """

        pipe_nodes: list = []
        asset_nodes: list = []
        pipe_asset_edges: list = []
        all_dma_data: list = []
        all_utility_data: list = []
        all_asset_node_labels: list = []

        for cnodes in consolidated_nodes:
            asset_nodes.append([])

            (
                pipe_node_data,
                asset_node_data,
                dma_data,
                utility_data,
                asset_node_labels,
            ) = self._create_pipe_asset_nodes(cnodes)

            if pipe_node_data:
                pipe_nodes.append(pipe_node_data)

            if asset_node_data:
                asset_nodes[-1].append(asset_node_data)

            ### create edges between junction/end node and the asset nodes
            ### that are at the same position
            pipe_asset_edges.extend(
                self._create_pipe_node_to_asset_node_edge(
                    pipe_nodes[-1], asset_nodes[-1]
                )
            )

            all_dma_data.extend(dma_data)
            all_utility_data.extend(utility_data)
            all_asset_node_labels.extend(asset_node_labels)

        return (
            pipe_nodes,
            asset_nodes,
            pipe_asset_edges,
            all_dma_data,
            all_utility_data,
            all_asset_node_labels,
        )

    def _get_edges_by_pipe(self, base_pipe, nodes_by_pipe):
        edges_by_pipe = []

        from_node = nodes_by_pipe[0]
        for to_node in nodes_by_pipe[1:]:

            from_node_pnt = Point(from_node["coords_27700"])
            to_node_pnt = Point(to_node["coords_27700"])
            line_geom = LineString(base_pipe["geometry"].coords)

            from_location = line_locate_point(line_geom, from_node_pnt)
            to_location = line_locate_point(line_geom, to_node_pnt)

            line_segment = substring(
                line_geom, from_location, to_location, normalized=True
            )

            if base_pipe["asset_label"] not in self.network_edge_labels:
                self.network_edge_labels.append(base_pipe["asset_label"])

            edges_by_pipe.append(
                {
                    "from_node_key": from_node["node_key"],
                    "to_node_key": to_node["node_key"],
                    "edge_key": f"{from_node['node_key']}-{to_node['node_key']}",
                    "tag": base_pipe["tag"],
                    "pipe_type": base_pipe["pipe_type"],
                    "material": base_pipe["material"],
                    "diameter": base_pipe["diameter"],
                    "asset_name": base_pipe["asset_name"],
                    "asset_label": base_pipe["asset_label"],
                    "dma_codes": base_pipe["dma_codes"],
                    "dma_names": base_pipe["dma_names"],
                    "dmas": base_pipe["dmas"],
                    "segment_length": round(line_segment.length, 5),
                    "segment_wkt": line_segment.wkt,
                }
            )
            from_node = to_node

        return edges_by_pipe

    def _set_nodes_and_edges(self, base_pipe, nodes_ordered):

        consolidated_nodes = self._consolidate_nodes_on_position(nodes_ordered)

        (
            nodes_by_pipe,
            asset_nodes_by_pipe,
            pipe_node_to_asset_node_edges,
            dma_data,
            utility_data,
            all_asset_node_labels,
        ) = self._set_network_node_and_edge_data(consolidated_nodes)

        # create edges between junction and end nodes for the pipe
        edges_by_pipe = self._get_edges_by_pipe(base_pipe, nodes_by_pipe)

        return (
            nodes_by_pipe,
            edges_by_pipe,
            asset_nodes_by_pipe,
            pipe_node_to_asset_node_edges,
            dma_data,
            utility_data,
            all_asset_node_labels,
        )

    def _get_base_pipe_data(self, qs_object) -> dict:
        base_pipe: dict = {}

        base_pipe["id"] = qs_object.pk
        base_pipe["tag"] = qs_object.tag
        base_pipe["pipe_type"] = qs_object.pipe_type
        base_pipe["asset_name"] = qs_object.asset_name
        base_pipe["asset_label"] = qs_object.asset_label
        base_pipe["pipe_length"] = qs_object.pipe_length
        base_pipe["wkt"] = qs_object.wkt
        base_pipe["material"] = qs_object.material
        base_pipe["diameter"] = qs_object.diameter
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

        base_pipe["line_start_intersection_tags"] = []
        base_pipe["line_start_intersection_ids"] = []
        for line in qs_object.line_start_intersections:
            base_pipe["line_start_intersection_tags"].extend(line["tags"])
            base_pipe["line_start_intersection_ids"].extend(line["ids"])

        base_pipe["line_start_intersection_tags"].remove(qs_object.tag)
        base_pipe["line_start_intersection_ids"].remove(qs_object.id)

        base_pipe["line_end_intersection_tags"] = []
        base_pipe["line_end_intersection_ids"] = []
        for line in qs_object.line_end_intersections:
            base_pipe["line_end_intersection_tags"].extend(line["tags"])
            base_pipe["line_end_intersection_ids"].extend(line["ids"])

        base_pipe["line_end_intersection_tags"].remove(qs_object.tag)
        base_pipe["line_end_intersection_ids"].remove(qs_object.id)

        # base_pipe["start_geom_latlong"] = qs_object.start_geom_latlong
        # base_pipe["end_geom_latlong"] = qs_object.end_geom_latlong

        # TODO: maybe convert base_pipe to simplenamespace
        # SimpleNamespace

        return base_pipe

    def _combine_all_pipe_junctions(self, pipe_qs_object) -> list:
        return pipe_qs_object.pipemain_junctions

    def _combine_all_point_assets(self, pipe_qs_object) -> list:
        return (
            pipe_qs_object.chamber_data
            + pipe_qs_object.operational_site_data
            + pipe_qs_object.network_meter_data
            + pipe_qs_object.logger_data
            + pipe_qs_object.hydrant_data
            + pipe_qs_object.pressure_fitting_data
            + pipe_qs_object.pressure_valve_data
            + pipe_qs_object.network_opt_valve
            + pipe_qs_object.connection_meter_data
            + pipe_qs_object.consumption_meter_data
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

        if self.neoj4_point:
            intersection_geom_4326 = intersection_geom.transform(4326, clone=True)

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
                        "intersection_point_geometry": GEOSGeometry(
                            f"POINT ({coords[0]} {coords[1]})", self.srid
                        ),
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
        termini_intersecting_pipe_tags = (
            base_pipe["line_start_intersection_tags"]
            + base_pipe["line_end_intersection_tags"]
        )

        non_termini_intersecting_pipes = [
            pipe
            for pipe in junctions_with_positions
            if pipe["tag"] not in termini_intersecting_pipe_tags
        ]

        # non_termini_intersecting_pipes.append(
        #     {
        #         "id": 1,
        #         "tag": 88888888,
        #         "distance_from_pipe_start_cm": 73,
        #         "intersection_point_geometry": base_pipe["start_point_geom"],
        #     }
        # )
        # non_termini_intersecting_pipes.append(
        #     {
        #         "id": 2,
        #         "tag": 333333,
        #         "distance_from_pipe_start_cm": 50,
        #         "intersection_point_geometry": base_pipe["start_point_geom"],
        #     }
        # )
        # non_termini_intersecting_pipes.append(
        #     {
        #         "id": 3,
        #         "tag": 999999,
        #         "distance_from_pipe_start_cm": 50,
        #         "intersection_point_geometry": base_pipe["start_point_geom"],
        #     }
        # )
        # non_termini_intersecting_pipes.append(
        #     {
        #         "id": 4,
        #         "tag": 77777,
        #         "distance_from_pipe_start_cm": 73,
        #         "intersection_point_geometry": base_pipe["start_point_geom"],
        #     }
        # )
        # non_termini_intersecting_pipes.append(
        #     {
        #         "id": 5,
        #         "tag": 111111,
        #         "distance_from_pipe_start_cm": 73,
        #         "intersection_point_geometry": base_pipe["start_point_geom"],
        #     }
        # )
        # non_termini_intersecting_pipes.append(
        #     {
        #         "id": 6,
        #         "tag": 222222,
        #         "distance_from_pipe_start_cm": 35,
        #         "intersection_point_geometry": base_pipe["start_point_geom"],
        #     }
        # )

        return non_termini_intersecting_pipes

    def _set_terminal_nodes(self, base_pipe):
        start_node_distance_cm = 0
        # round to int to make distance comparisons more robust
        end_node_distance_cm = round(base_pipe["pipe_length"].cm)

        line_start_intersection_tags = base_pipe["line_start_intersection_tags"]
        line_end_intersection_tags = base_pipe["line_end_intersection_tags"]

        start_node_tags = sorted([base_pipe["tag"], *line_start_intersection_tags])
        end_node_tags = sorted([base_pipe["tag"], *line_end_intersection_tags])

        if not line_start_intersection_tags:
            start_node_type = PIPE_END__NAME
        else:
            start_node_type = PIPE_JUNCTION__NAME

        if not line_end_intersection_tags:
            end_node_type = PIPE_END__NAME
        else:
            end_node_type = PIPE_JUNCTION__NAME

        nodes_ordered = [
            {
                "pipe_tags": start_node_tags,
                "node_type": start_node_type,
                "distance_from_pipe_start_cm": start_node_distance_cm,
                "dma_codes": base_pipe["dma_codes"],
                "dma_names": base_pipe["dma_names"],
                "dmas": base_pipe["dma_codes"],
                "intersection_point_geometry": base_pipe["start_point_geom"],
                "utility_name": self._get_utility(base_pipe),
                **base_pipe,
            },
            {
                "pipe_tags": end_node_tags,
                "node_type": end_node_type,
                "distance_from_pipe_start_cm": end_node_distance_cm,
                "dma_codes": base_pipe["dma_codes"],
                "dma_names": base_pipe["dma_names"],
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
            pipe_tag = pipe["tag"]
            # distance_from_start_cm must be an
            # int for sqid compatible hashing
            distance_from_pipe_start_cm = pipe["distance_from_pipe_start_cm"]

            tags = sorted([pipe_tag, base_pipe["tag"]])
            if distance_from_pipe_start_cm not in distances:

                position_index = bisect.bisect_right(
                    nodes_ordered,
                    distance_from_pipe_start_cm,
                    key=lambda x: x["distance_from_pipe_start_cm"],
                )

                nodes_ordered.insert(
                    position_index,
                    {
                        "pipe_tags": tags,
                        "node_type": PIPE_JUNCTION__NAME,
                        "utility_name": self._get_utility(base_pipe),
                        "distance_from_pipe_start_cm": distance_from_pipe_start_cm,
                        "dma_codes": base_pipe["dma_codes"],
                        "dma_names": base_pipe["dma_names"],
                        "dmas": base_pipe["dmas"],
                        "intersection_point_geometry": pipe[
                            "intersection_point_geometry"
                        ],
                        **base_pipe,
                    },
                )

                distances.append(distance_from_pipe_start_cm)
            else:
                nodes_ordered[position_index]["pipe_tags"].append(pipe_tag)
                nodes_ordered[position_index]["pipe_tags"] = sorted(
                    nodes_ordered[position_index]["pipe_tags"]
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
                    "dma_codes": base_pipe["dma_codes"],
                    "dma_names": base_pipe["dma_names"],
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

    def _encode_node_key(self, point, extra_params=[]):
        """
        Round and cast Point geometry coordinates to str to remove '.'
        then return back to int to make make coords sqid compatible.

        Note these are not coordinates but int representations of the
        coordinates to ensure a unique node_key.
        """

        coord1_repr = int(str(round(point.coords[0], 3)).replace(".", ""))
        coord2_repr = int(str(round(point.coords[1], 3)).replace(".", ""))
        return self.sqids.encode([coord1_repr, coord2_repr, *extra_params])
