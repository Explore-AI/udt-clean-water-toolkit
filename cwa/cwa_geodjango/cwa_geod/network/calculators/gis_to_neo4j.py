import json
from multiprocessing.pool import ThreadPool
from django.db import connections
from django.db.models.query import QuerySet
from django.contrib.gis.geos import Point
from neomodel.contrib.spatial_properties import NeomodelPoint
from neomodel.exceptions import UniqueProperty, ConstraintValidationFailed
from cleanwater.exceptions import (
    InvalidNodeException,
    InvalidPipeException,
)
from . import GisToGraph
from cwa_geod.core.constants import (
    TRUNK_MAIN__NAME,
    DISTRIBUTION_MAIN__NAME,
    PIPE_END__NAME,
    POINT_ASSET__NAME,
)
from ..models import PointAsset, PipeEnd
from timeit import default_timer as timer


class GisToNeo4J(GisToGraph):
    """Create a Neo4J graph of assets from a geospatial
    network of assets"""

    def __init__(self, config):
        self.config = config
        super().__init__(config)

    def create_network(self):
        pipes_qs = self.get_pipe_and_asset_data()

        if not self.config.query_limit:
            query_limit = self.get_pipe_count(pipes_qs)
        else:
            query_limit = self.config.query_limit

        if not self.config.query_offset:
            query_offset = 0

        for offset in range(query_offset, query_limit, self.config.query_step):
            limit = offset + self.config.query_step

            sliced_qs = list(pipes_qs[offset:limit])

            self.calc_pipe_point_relative_positions(sliced_qs)

            # self._create_neo4j_graph()

    def _generate_slices(self, pipes_qs):
        slices = []

        initial_slice = self.offset
        final_slice = self.offset + self.limit
        skip_slice = self.step

        start_slice = initial_slice
        for start_slice in range(initial_slice, final_slice, skip_slice):
            end_slice = start_slice + skip_slice
            print(start_slice, end_slice)
            slices.append(
                (pipes_qs[start_slice:end_slice]),
            )

        return slices

    def create_network_parallel(self):
        def _map_pipe_assets_calcs_parallel(pipes_qs):
            new_connection = connections.create_connection("default")
            values = list(pipes_qs)
            new_connection.close()
            return values

        start = timer()
        print("0")
        pipes_qs = self.get_pipe_and_asset_data()

        pipes_qs_slices = self._generate_slices(pipes_qs)

        connections.close_all()
        print("a")
        with ThreadPool(4) as p:
            qs_data = p.map(_map_pipe_assets_calcs_parallel, pipes_qs_slices)
        print("b")
        qs_values_list = []
        int = timer()
        print(int - start)
        for qs in qs_data:
            qs_values_list += qs
        print("c")
        int2 = timer()
        print(int2 - start)

        self.calc_pipe_point_relative_positions_parallel(qs_values_list)

        # procs = []
        # for slice in slices:
        #     proc = Process(target=_map_pipe_assets_calcs_parallel, args=(slice))
        #     procs.append(proc)
        #     proc.start()

        # for proc in procs:
        #     proc.join()

        end = timer()
        print(end - start)
        import pdb

        pdb.set_trace()
        self._create_neo4j_graph_parallel()

    def get_pipe_and_asset_data(self):
        trunk_mains_qs: QuerySet = self.get_trunk_mains_data()
        distribution_mains_qs: QuerySet = self.get_distribution_mains_data()

        pipes_qs: QuerySet = trunk_mains_qs.union(distribution_mains_qs, all=True)
        return pipes_qs

    @staticmethod
    def build_dma_data_as_json(dma_codes, dma_names):
        dma_data = [
            {"code": dma_code, "name": dma_name}
            for dma_code, dma_name in zip(dma_codes, dma_names)
        ]

        return json.dumps(dma_data)

    def check_node_exists(self, asset_name, gid):
        node_type: str = self._get_node_type(asset_name)

        if node_type == PIPE_END__NAME:
            node = PipeEnd.nodes.get_or_none(pipe_type=asset_name, gid=gid)
            return node, node_type, None
        elif node_type == POINT_ASSET__NAME:
            asset_model = PointAsset.asset_name_model_mapping(asset_name)

            node = asset_model.nodes.get_or_none(gid=gid)
            return node, node_type, asset_model
        else:
            InvalidNodeException(
                f"Invalid node detected: {node_type}. Valid nodes are {PIPE_END__NAME} or {POINT_ASSET__NAME}"
            )

    @staticmethod
    def _connect_nodes(start_node, end_node, pipe_name, relation_data):
        try:
            if pipe_name == TRUNK_MAIN__NAME:
                start_node.trunk_main.connect(end_node, relation_data)
            elif pipe_name == DISTRIBUTION_MAIN__NAME:
                start_node.distrbution_main.connect(end_node, relation_data)
            else:
                InvalidPipeException(f"Invalid pipe detected: {pipe_name}.")
        except ConstraintValidationFailed:
            pass

    def _create_and_connect_pipe_end_node(
        self, pipe_name, gid, asset_name, dma_data, start_node
    ):
        try:
            pipe_end = PipeEnd.create(
                {
                    "gid": gid,
                    "dmas": dma_data,
                    "pipe_type": asset_name,
                    #                        "location": coords,
                }
            )[0]
        except UniqueProperty:
            pipe_end = PipeEnd.nodes.get_or_none(pipe_type=asset_name, gid=gid)

        self._connect_nodes(
            start_node,
            pipe_end,
            pipe_name,
            {"dmas": dma_data, "gid": gid, "weight": 1},
        )

        return pipe_end

    def _create_and_connect_point_asset_node(
        self, pipe_name, gid, asset_model, dma_data, start_node
    ):
        try:
            point_asset = asset_model.create(
                {
                    "gid": gid,
                    "dmas": dma_data,
                    #                       "location": coords,
                }
            )[0]
        except UniqueProperty:
            point_asset = asset_model.nodes.get_or_none(gid=gid)

        # edge_length: float = node_point_geometries[-1].distance(
        #     asset["intersection_point_geometry"]
        # )

        # TODO: add wieght to relation based on edge length

        self._connect_nodes(
            start_node,
            point_asset,
            pipe_name,
            {"dmas": dma_data, "gid": gid, "weight": 1},
        )

        return point_asset

    def _set_connected_asset_relations(
        self, pipe_data: dict, assets_data: list, pipe_end
    ) -> None:
        start_node = pipe_end

        for asset in assets_data:
            gid: int = asset["data"]["gid"]
            asset_name: str = asset["data"]["asset_name"]
            dma_data = self.build_dma_data_as_json(
                asset["data"]["dma_codes"], asset["data"]["dma_names"]
            )

            pipe_name = pipe_data["asset_name"]

            # point = asset["intersection_point_geometry"].transform("WGS84", clone=True)

            # coords = NeomodelPoint((point.x, point.y), crs="wgs-84")

            node, node_type, asset_model = self.check_node_exists(asset_name, gid)

            if not node and node_type == PIPE_END__NAME:
                start_node = self._create_and_connect_pipe_end_node(
                    pipe_name, gid, asset_name, dma_data, start_node
                )
            elif not node and node_type == POINT_ASSET__NAME:
                start_node = self._create_and_connect_point_asset_node(
                    pipe_name, gid, asset_model, dma_data, start_node
                )

            elif node_type not in [PIPE_END__NAME, POINT_ASSET__NAME]:
                raise InvalidNodeException(
                    f"Invalid node detected: {node_type}. Valid nodes are {PIPE_END__NAME} or {POINT_ASSET__NAME}"
                )

    def _map_pipe_connected_asset_relations(self, pipe_data: dict, assets_data: list):
        pipe_gid = pipe_data.get("gid")
        pipe_type = pipe_data.get("asset_name")

        #
        pipe_end = PipeEnd.nodes.get_or_none(pipe_type=pipe_type, gid=pipe_gid)

        if not pipe_end:
            dma_data = self.build_dma_data_as_json(
                pipe_data["dma_codes"], pipe_data["dma_names"]
            )

            # point = Point(pipe_data["geometry"][0][0], srid=DEFAULT_SRID).transform(
            #     "WGS84", clone=True
            # )

            # coords = NeomodelPoint((point.x, point.y), crs="wgs-84")

            try:
                pipe_end = PipeEnd.create(
                    {
                        "gid": pipe_gid,
                        "dmas": dma_data,
                        "pipe_type": pipe_type,
                        #                        "location": coords,
                    }
                )[0]
            except UniqueProperty:
                pipe_end = PipeEnd.nodes.get_or_none(pipe_type=pipe_type, gid=pipe_gid)

        self._set_connected_asset_relations(pipe_data, assets_data, pipe_end)

    def _create_neo4j_graph(self) -> None:
        """Iterate over pipes and connect related pipe interactions
        and point assets. Uses a map method to operate on the pipe
        and asset data.

        Params:
              None
        Returns:
              None
        """

        list(
            map(
                self._map_pipe_connected_asset_relations,
                self.all_pipe_data,
                self.all_asset_positions,
            )
        )

    def _create_neo4j_graph_parallel(self) -> None:
        """Same as _create_neo4j_graph() except done in a multithreaded manner

        https://github.com/neo4j-contrib/neomodel/blob/master/test/test_multiprocessing.py

        Params:
              None
        Returns:
              None
        """

        items = zip(self.all_pipe_data, self.all_asset_positions)

        with ThreadPool(4) as p:
            p.starmap(self._map_pipe_connected_asset_relations, items)

        # with mp.pool.ThreadPool(5) as p:
        #     p.map(self._create_neo4j_graph, range(50))
