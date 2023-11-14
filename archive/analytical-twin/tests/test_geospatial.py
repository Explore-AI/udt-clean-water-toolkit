import pyproj
from shapely.geometry import Polygon
import geopandas as gpd

import data_factory.AnalyticalTwin.geospatial as geospatial
from data_factory.AnalyticalTwin.analytical_twin import CleanTwin


class TestChartModule:
    @classmethod
    def setup(cls):
        twin = CleanTwin(analytical_twin_folder='examples/AnalyticalTwin')
        twin.load_graph()
        cls.test_graph = twin

    def test_chart_network(self):
        twin = self.test_graph
        geospatial.nodes_to_gdf(twin)

    def test_subset_on_polygon(self):
        twin = self.test_graph
        polygon = Polygon(((530000, 170000),
                          (540000, 170000),
                          (540000, 180000),
                          (530000, 180000)))
        subset_twin = geospatial.subgraph_on_polygon(twin, polygon)
        assert len(subset_twin.edges()) == 10455

    def test_subset_on_geodataframe(self):
        twin = self.test_graph
        polygon = Polygon(((530000, 170000),
                           (540000, 170000),
                           (540000, 180000),
                           (530000, 180000)))
        crs = pyproj.CRS(27700)
        polygon_gdf = gpd.GeoDataFrame([1],
                                       geometry=gpd.geoseries.from_shapely(
                                           [polygon]),
                                       crs=crs)
        subset_twin = geospatial.subgraph_on_geodataframe(twin, polygon_gdf)
        assert len(subset_twin.edges()) == 10455
