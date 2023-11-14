import json

import folium
from geopandas import GeoDataFrame
from shapely.geometry import Point, mapping

from data_factory.AnalyticalTwin.analytical_twin import Twin
from data_factory.AnalyticalTwin.chart import get_xy, get_graph_center_coords
from data_factory.AnalyticalTwin.geospatial import convert_coordinates


def add_polygon(m: folium.Map, gdf: GeoDataFrame):
    """

    :param m:
    :type m: folium.Map

    :param dma_gdf:
    :type dma_gdf: GeoDataFrame

    :return: None
    """
    for x in gdf.iterrows():
        folium.GeoJson(x[1]['geojson']).add_to(m)


def add_edge(m: folium.Map, graph: Twin, node1: str, node2: str,
             colour="orange", tooltip=None):
    """
    Adds an edge from a twin into a folium basemap

    :param m: The folium base map to add the edge too
    :type m: folium.Map

    :param graph: The twin to get the data from for the edge geospatial
     information
    :type graph: Twin

    :param node1: The starting node of the edge
    :type node1: str

    :param node2: The ending node of the edge
    :type node2: str

    :param colour: The colour of the edge
    :type colour: str

    :param tooltip: The string to display on the tooltip of the edge
    :type tooltip: str

    :return: None
    """
    details1 = graph.nodes(data=True)[node1]
    lon1, lat1 = get_xy(details1)
    lon1, lat1 = convert_coordinates(lon1, lat1)

    details2 = graph.nodes(data=True)[node2]
    lon2, lat2 = get_xy(details2)
    lon2, lat2 = convert_coordinates(lon2, lat2)

    folium.PolyLine([(lat1, lon1), (lat2, lon2)],
                    color=colour, tooltip=tooltip).add_to(m)


def add_node(m: folium.Map, graph: Twin, node: str,
             colour: str, tooltip: str = None):
    """
    Adds a node from a twin into a folium basemap

    :param m: The folium base map to add the node to
    :type m: folium.Map

    :param graph: The twin to get the data from for the nodes geospatial
     information
    :type graph: Twin

    :param node: The node if of the node to add to the map
    :type node1: str

    :param colour: The colour of the node
    :type colour: str

    :param tooltip: The string to display on the tooltip of the node
    :type tooltip: str

    :return: None
    """
    node_data = graph.nodes(data=True)[node]
    lon, lat = get_xy(node_data)
    lon, lat = convert_coordinates(lon, lat)
    p = Point(lon, lat)

    folium.GeoJson(json.dumps(mapping(p)),
                   marker=folium.CircleMarker(radius=4, weight=0,
                                              fill_color=colour,
                                              fill_opacity=1),
                   tooltip=tooltip).add_to(m)


def plot_twin(graph: Twin) -> folium.Map:
    """
    Plot all the edges and nodes in a twin. Note no colours are applied.

    :param graph: A twin to be plotted. Note this should be subset from the
    main twin. Folium is not designed to plot 2e6 entities
    :type graph: Twin

    :return: A folium map with all the twins edges and nodes added
    :rtype: folium.Map
    """

    x, y = get_graph_center_coords(graph)

    y, x = convert_coordinates(y, x)

    m = folium.Map(location=[x, y], zoom_start=10)
    for node1, node2 in list(graph.edges):
        add_edge(m, graph, node1, node2)

    for node in list(graph.nodes):
        add_node(m, graph, node, 'black')

    return m
