import pytest
import joblib
from sqids import Sqids
from django.contrib.gis.geos import GEOSGeometry

# from shapely import wkt
import pandas as pd
import geopandas as gpd
from .data.gis_to_graph_data import (
    PIPE_JUNCTIONS,
    POINT_ASSETS,
    JUNCTIONS_WITH_POSITIONS,
    POINT_ASSETS_WITH_POSITIONS,
    NODES_ORDERED,
)

from cleanwater.transform.gis_to_graph import GisToGraph


BASE_PIPE_DATA_FILE_PATH = "./data/base_pipe_data.csv"

sqids = Sqids(alphabet="86QDHYuRxW3OfckshvCUtngEKamBbrPGNiM9LwjFypVq1Ze0TSIl4Jz5X2dA7o")

SRID = 27700


@pytest.mark.skip(reason="This function received the test input data.")
def get_pipe_data():

    gdf = gpd.read_file(BASE_PIPE_DATA_FILE_PATH)
    gdf.crs = "epsg:27700"
    base_pipe = gdf.to_dict("records")[0]

    base_pipe["geometry"] = GEOSGeometry(base_pipe["wkt"], SRID)

    import pdb

    pdb.set_trace()

    return base_pipe


# content of test_class.py
class TestGisToGraph:

    def test_get_junction_connections_on_pipe(self):
        base_pipe = get_pipe_data()

        gis_to_graph = GisToGraph(SRID, sqids)
        junctions_with_positions = gis_to_graph._get_connections_points_on_pipe(
            base_pipe, PIPE_JUNCTIONS
        )

        del junctions_with_positions[0]["intersection_point_geometry"]
        del junctions_with_positions[1]["intersection_point_geometry"]
        assert junctions_with_positions == JUNCTIONS_WITH_POSITIONS

    def test_get_connections_points_on_pipe(self):

        base_pipe = get_pipe_data()

        gis_to_graph = GisToGraph(SRID, sqids)

        point_assets_with_positions = gis_to_graph._get_connections_points_on_pipe(
            base_pipe, JUNCTIONS_WITH_POSITIONS
        )

        del point_assets_with_positions[0]["intersection_point_geometry"]
        del point_assets_with_positions[1]["intersection_point_geometry"]
        assert point_assets_with_positions == POINT_ASSETS_WITH_POSITIONS

    def test_set_node_properties(self):

        base_pipe = get_pipe_data()
        gis_to_graph = GisToGraph(SRID, sqids)

        # Get the intersection points of all intersecting pipes (pipe junctions)
        junctions_with_positions = gis_to_graph._get_connections_points_on_pipe(
            base_pipe,
            PIPE_JUNCTIONS,
        )
        print("78")
        # Get the intersection points of all point assets
        point_assets_with_positions = gis_to_graph._get_connections_points_on_pipe(
            base_pipe,
            POINT_ASSETS,
        )

        print("ok")
        nodes_ordered = gis_to_graph._set_node_properties(
            base_pipe, junctions_with_positions, point_assets_with_positions
        )

        geometries = [
            "intersection_point_geometry",
            "geometry",
            "start_point_geom",
            "end_point_geom",
        ]

        for geom in nodes_ordered:
            for geometry in geometries:
                if geometry in geom:
                    del nodes_ordered[geometry]

        assert nodes_ordered == NODES_ORDERED

    # def test_set_node_properties(self):

    #     base_pipe = get_pipe_data()

    #     gis_to_graph = GisToGraph(SRID, sqids)

    #     nodes_ordered = gis_to_graph._set_node_properties(
    #         base_pipe, JUNCTIONS_WITH_POSITIONS, POINT_ASSETS_WITH_POSITIONS
    #     )

    #     print(nodes_ordered)
