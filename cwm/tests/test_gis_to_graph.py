import pytest
import joblib
from sqids import Sqids
from django.contrib.gis.geos import GEOSGeometry

# from shapely import wkt
# import pandas as pd
import geopandas as gpd
from .data.pipe_junctions_data import ALL_PIPE_JUNCTIONS
from .data.point_asset_data import ALL_POINT_ASSETS
from cleanwater.transform.gis_to_graph import GisToGraph


BASE_PIPE_DATA_FILE_PATH = "./data/base_pipe_data.csv"

sqids = Sqids(alphabet="86QDHYuRxW3OfckshvCUtngEKamBbrPGNiM9LwjFypVq1Ze0TSIl4Jz5X2dA7o")

SRID = 27700


@pytest.mark.skip(reason="This function received the test input data.")
def get_pipe_data():
    gdf = gpd.read_file(BASE_PIPE_DATA_FILE_PATH)
    gdf.crs = "epsg:27700"
    base_pipes = gdf.to_dict("records")

    for i, base_pipe in enumerate(base_pipes):
        base_pipes[i]["geometry"] = GEOSGeometry(base_pipe["wkt"], SRID)

    return base_pipes


# content of test_class.py
class TestGisToGraph:

    def test_get_junction_connections_on_pipe(self):
        expected_junctions_with_positions_hash = "5ab6d931f1ef39e38202fa77844375ef"
        base_pipes = get_pipe_data()

        gis_to_graph = GisToGraph(SRID, sqids)

        for base_pipe, pipe_junctions in zip(base_pipes, ALL_PIPE_JUNCTIONS):
            junctions_with_positions = gis_to_graph._get_connections_points_on_pipe(
                base_pipe, pipe_junctions
            )

            assert (
                joblib.hash(junctions_with_positions)
                == expected_junctions_with_positions_hash
            )
            break

    def test_get_assets_connections_on_pipe(self):
        expected_point_assets_with_positions_hash = "0a7fdad5f5ecfb3571f9755d57e965bd"

        base_pipes = get_pipe_data()

        gis_to_graph = GisToGraph(SRID, sqids)

        for base_pipe, point_assets in zip(base_pipes, ALL_POINT_ASSETS):
            point_assets_with_positions = gis_to_graph._get_connections_points_on_pipe(
                base_pipe, point_assets
            )

            assert (
                joblib.hash(point_assets_with_positions)
                == expected_point_assets_with_positions_hash
            )
            break


# TestGisToGraph()
# get_pipe_data()


# df = pd.read_csv(BASE_PIPE_DATA_FILE_PATH)
# df["geometry"] = df["geometry"].apply(wkt.loads)
# gdf = gpd.GeoDataFrame(df, crs="epsg:27700")

# gdf = gpd.GeoDataFrame(
#     df,
#     geometry=gpd.points_from_xy(df.Longitude, df.Latitude),
#     crs="EPSG:27700",
# )
