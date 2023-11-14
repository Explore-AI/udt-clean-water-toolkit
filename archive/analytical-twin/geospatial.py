from typing import Union

import pandas as pd
import geopandas as gpd
import pyproj
from shapely import wkt
from shapely.geometry import Point, Polygon, base
from shapely.ops import transform

from data_factory.AnalyticalTwin.analytical_twin import Twin
from data_factory.AnalyticalTwin.chart import get_xy
from data_factory.geospatial.functions import load_geospatial_table


def nodes_to_gdf(g: Twin, crs: pyproj.CRS = pyproj.CRS('epsg:27700')) -> \
        gpd.GeoDataFrame:
    """
    Extracts the geospatial data from the clean twin and return it as a
    geodataframe.

    :param g: Twin to convert to a geodataframe
    :type g: Twin

    :param crs: The CRS of the data within the twin
    :type crs: pyproj.CRS

    :return: A geodataframe with all the nodes from the twin in it
    :rtype: GeoDataFrame
    """

    nodes_xy = [(x[0], f"POINT ({get_xy(x[1])[0]} {get_xy(x[1])[1]})")
                for x in g.nodes(data=True)]
    nodes_df = pd.DataFrame(nodes_xy, columns=['node', 'geometry'])

    nodes_df['geometry'] = nodes_df['geometry'].apply(wkt.loads)
    return gpd.GeoDataFrame(nodes_df, geometry='geometry', crs=pyproj.CRS(crs))


def convert_crs(geometry: base,
                from_crs: pyproj.CRS = pyproj.CRS('epsg:27700'),
                to_crs: pyproj.CRS = pyproj.CRS('epsg:4326')) -> base:
    """
    Converts a shapely geometry into a different CRS

    :param geometry: A geometry to convert
    :param from_crs: the source CRS
    :param to_crs: the target CRS
    :return: The geometry converted into the target CRS
    """
    project = pyproj.Transformer.from_crs(from_crs, to_crs,
                                          always_xy=True).transform
    return transform(project, geometry)


def convert_coordinates(x: Union[int, float], y: Union[int, float],
                        from_crs: pyproj.CRS = pyproj.CRS('epsg:27700'),
                        to_crs: pyproj.CRS = pyproj.CRS('epsg:4326')) -> \
        (float, float):
    """
    Converts a pair of coordinates into a different CRS

    :param x: A x coordinate to convert
    :param y: A y coordinate to convert
    :param from_crs: the source CRS
    :param to_crs: the target CRS
    :return: The geometry converted into the target CRS
    """
    point = Point(x, y)
    point = convert_crs(point, from_crs=from_crs, to_crs=to_crs)
    return point.x, point.y


def subgraph_on_geodataframe(graph: Twin, gdf: gpd.GeoDataFrame) -> \
        gpd.GeoDataFrame:
    """
    Creates a subgraph of the twin based on a geodataframe of polygons. This
    geodataframe is joined using the binary predicate 'intersects'.

    :param graph: the twin to subgraph
    :param gdf: a geodataframe containing an area of interest to subset the
        twin on
    :return: a subsetted twin with all nodes within the geodataframe
    """
    nodes_gdf = nodes_to_gdf(graph)
    regions_nodes_gdf = gpd.sjoin(nodes_gdf, gdf, how='inner')
    regions_node_ids = regions_nodes_gdf['node'].to_list()
    region_subgraph = graph.subgraph(regions_node_ids)
    return region_subgraph


def subgraph_on_polygon(graph: Twin, polygon: Polygon,
                        crs: pyproj.CRS = pyproj.CRS(27700)):
    """
    Creates a subgraph of the twin based on a polygon. This
    polygon is joined using the binary predicate 'intersects' and geopandas

    :param graph: the twin to subgraph
    :param polygon: a geodataframe containing an area of interest to subset the
        twin on
    :param crs: the crs of the polygon
    :return: a subsetted twin with all nodes within the geodataframe
    """
    polygon_gdf = gpd.GeoDataFrame([1],
                                   geometry=gpd.geoseries.from_shapely(
                                       [polygon]),
                                   crs=crs)

    return subgraph_on_geodataframe(graph, polygon_gdf)


def subset_on_dma(graph: Twin, dma_code: str,
                  table_name: str = 'cwbdma',
                  schema_name: str = 'dpsn_sources'):
    """
    Creates a subgraph of the twin based on a dma area from the data table.
    This needs to be saved as a raw table with the geometry converted to wkt in
    the column named WKT.

    :param graph: the twin to subgraph
    :param dma_code: the code of the dma
    :param table_name: the schema which the dma table is stored in
    :param schema_name: the table name of the dma table
    :return: a subsetted twin with all nodes within the dma
    """
    dma_gdf = load_geospatial_table(table_name, schema_name,
                                    columns=['wkt', 'DMAAREACODE'])
    dma_gdf = dma_gdf[dma_gdf['DMAAREACODE'] == dma_code]

    subgraph = subgraph_on_geodataframe(graph, dma_gdf)
    return subgraph
