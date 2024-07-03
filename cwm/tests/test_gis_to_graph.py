import pytest
from shapely import wkt
import pandas as pd
import geopandas as gpd
from .data.pipe_junctions_data import PIPE_JUNCTIONS
from .data.point_asset_data import POINT_ASSETS


BASE_PIPE_DATA_FILE_PATH = "./data/base_pipe_data.csv"


@pytest.mark.skip(reason="This function received the test input data.")
def get_pipe_data():
    gdf = gpd.read_file(BASE_PIPE_DATA_FILE_PATH)
    gdf.crs = "epsg:27700"

    return gdf.to_dict("records")


# content of test_class.py
class TestGisToGraph:

    def test_get_connections_points_on_pipe(self):
        base_pipes = get_pipe_data()

        for base_pipe, pipe_junction, point_asset in zip(
            base_pipes, PIPE_JUNCTIONS, POINT_ASSETS
        ):
            print(base_pipe)
            print(pipe_junction)
            print(point_asset)

            x = "this"
            assert "h" in x


# TestGisToGraph()


# df = pd.read_csv(BASE_PIPE_DATA_FILE_PATH)
# df["geometry"] = df["geometry"].apply(wkt.loads)
# gdf = gpd.GeoDataFrame(df, crs="epsg:27700")

# gdf = gpd.GeoDataFrame(
#     df,
#     geometry=gpd.points_from_xy(df.Longitude, df.Latitude),
#     crs="EPSG:27700",
# )
