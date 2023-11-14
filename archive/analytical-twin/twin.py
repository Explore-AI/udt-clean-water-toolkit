import pandas as pd
from typing import Union
from os.path import splitext
from shutil import copyfile
import uuid

from networkx import NetworkXNotImplemented
from shapely import wkt
from shapely.geos import WKTReadingError
from pathlib import Path
from data_factory.azure_data_factory.utils import dbfs_to_python, \
    python_to_dbfs
try:
    import networkx as nx
except ImportError:
    raise ImportError(
        "The networkx package is required to make use of the graph module. "
        "You can install it using 'conda install -c conda-forge networkx' or "
        "'pip install networkx'."
    )


def summarise_graph(graph: nx.Graph, data: str = 'layer') -> dict:
    """ counts the number of items in the data attribute """
    summary = dict()

    metadata = ['source_shape', 'source_gdb', 'run_name', 'creator']

    for m in metadata:
        summary[m] = graph.graph[m] if m in graph.graph.keys() else ''

    for _, d in graph.nodes(data=data):
        if d in summary.keys():
            summary[d] += 1
        else:
            summary[d] = 1

    for _, _, d in graph.edges(data=data):
        if d in summary.keys():
            summary[d] += 1
        else:
            summary[d] = 1
    return summary


def summarise_graphs(graphs: Union[dict, list]) -> pd.DataFrame:
    """" summarise multiple graphs into a dataframe"""

    if type(graphs) == list:
        graphs = {g.name: g for g in graphs}

    series = []
    for k, v in graphs.items():
        s = summarise_graph(v)
        series.append(pd.Series(s, name=k))

    return pd.DataFrame(series).T.reset_index()


def get_graph(file_name: str, folder: Union[str, Path]) -> nx.Graph:
    """
    Retreives a graph object from a folder.
    Mainly written to save to an adls folder

    Params
    ======
    file_name (str): file name to give the saved graph with an extension
    folder (str, pathlib.Path): the path to the folder to save the object.
        This should start dbfs:/

    Returns
    =======
    graph (nx.Graph): the graph object read
    """
    if not isinstance(folder, Path):
        folder = Path(folder)

    folder = dbfs_to_python(folder)

    unique_reference = str(uuid.uuid4()).replace('-', '')
    temp_file_name = splitext(file_name)[0] + unique_reference + '.pkl'
    temp_file_path = Path("/tmp/") / temp_file_name
    temp_file_path.parent.mkdir(parents=True, exist_ok=True)

    copyfile(folder / file_name, temp_file_path)
    g = nx.read_gpickle(temp_file_path)
    temp_file_path.unlink()

    # convert graph edge geometries to shapely.geometry:
    g = convert_edge_geometry(g, wkt_to_geom=True)
    return g


def save_graph(graph: nx.Graph, file_name: str, folder: str) -> str:
    """
    Saves graph object to temp folder then copies to twin folder in ADLS

    Params
    ======
    graph (nx.Graph): graph object to save
    name (str): filename to save graph under
    debug (bool): appends a 'dev' suffix to the filename
        To prevent overwriting a working Twin during development

    Returns
    =======
    folder (str): folder twin saved under
    filename (str): twin filename
    """

    if not isinstance(folder, Path):
        folder = Path(folder)

    if '.pkl' not in file_name:
        file_name += '.pkl'

    folder = dbfs_to_python(folder)
    folder.mkdir(parents=True, exist_ok=True)
    # convert graph edge geometries to WKT before pickling:
    graph = convert_edge_geometry(graph, geom_to_wkt=True)
    nx.write_gpickle(graph, folder / file_name)

    return python_to_dbfs(folder).as_posix(), file_name


def convert_edge_geometry(graph: nx.Graph,
                          geom_to_wkt: bool = False,
                          wkt_to_geom: bool = False) -> nx.Graph:
    """
    Converts the geometry attributes of the edges of a graph between
    shapely.geometry objects and Well Known Text (WKT) string format.
    Graph edges without geometry attributes are ignored.

    If geom_to_wkt is True, convert geometry objects to WKT:
    - Geometry attributes which do not have a '_geom' attribute are assumed to
      be in WKT format already, and are not modified.

    If wkt_to_geom is True, convert WKT to geometry objects:
    - Geometry attributes which are not a string are assumed to be
      shapely.geometry objects, and are not modified.
    - An error is raised if the string in the geometry attribute could
      not be parsed as WKT.

    If both (or neither) boolean is specified, an exception is raised.

    Note, this is an inplace conversion.

    Params
    ======
        graph (nx.Graph): networkx graph with edge geometry as shapely.geometry
                objects and/or WKT strings.
        geom_to_wkt (bool, optional): If true, convert geometry objects to WKT.
                Defaults to False.
        wkt_to_geom (bool, optional): If true, convert WKT to geometry objects.
                Defaults to False.

    Returns
    =======
        nx.Graph: networkx graph with edge geometry as shapely.geometry
                objects or WKT strings.
    """
    # check which conversion direction is specified:
    if geom_to_wkt and wkt_to_geom:
        # we can't do both conversions, raise exception
        raise Exception("Please choose either geom_to_wkt=True, "
                        "or wkt_to_geom=True, and not both")
    elif not geom_to_wkt and not wkt_to_geom:
        # we must specify at least one conversion, raise exception
        raise Exception("Please choose either geom_to_wkt=True, "
                        "or wkt_to_geom=True")

    # check type of nx.Graph:
    # note Multi(Di)Graph is a subclass of (Di)Graph, so order of isinstance
    # checks is important
    if isinstance(graph, (nx.MultiDiGraph, nx.MultiGraph)):
        # if an edge does not have a geometry attribute, the 'default=None'
        # prevents a KeyError
        # MultiGraphs and MultiDiGraphs have keys in their edges
        u_v_key_geom_list = [x for x in graph.edges(
            keys=True, data='geometry', default=None)]
    elif isinstance(graph, (nx.DiGraph, nx.Graph)):
        # if an edge does not have a geometry attribute, the 'default=None'
        # prevents a KeyError
        # Graphs and Digraphs do not have keys in their edges
        u_v_key_geom_list = [x for x in graph.edges(
            data='geometry', default=None)]
    else:
        # graph is not a networkx graph, raise TypeError
        raise TypeError("The provided graph was not a networkx graph "
                        "and was not modified.")

    # iterate over the edges in graph:
    for u_v_key_geom in u_v_key_geom_list:
        # the nodes (u,v), and key (for multigraphs)
        u_v_key = u_v_key_geom[0:-1]
        # the geometry attribute of the edge:
        geom = u_v_key_geom[-1]
        if geom is not None:
            if geom_to_wkt:
                # attempt to convert from geometry to WKT
                # using shapely.wkt.dumps:
                try:
                    graph.edges[u_v_key]['geometry'] = wkt.dumps(geom)
                except AttributeError:
                    # the geometry attribute was not a shapely.geometry object
                    # and could not be converted
                    # the most likely case is it is already a WKT string and
                    # so we make no changes
                    pass
            elif wkt_to_geom:
                if geom is not None:
                    # attempt to convert from WKT to geometry
                    # using shapely.wkt.loads:
                    try:
                        graph.edges[u_v_key]['geometry'] = wkt.loads(geom)
                    except TypeError:
                        # the geometry attribute was not a string
                        # the most likely case is it is already a
                        # shapely.geometry object and so we make no changes
                        pass
                    except WKTReadingError:
                        # the string could not be parsed, raise an error
                        raise

    return graph


def get_edges_attribute_set(graph: nx.Graph, attribute: str) -> set:
    """
    Returns the set of selected attribute for edges in the twin

    :param graph: NetworkX graph object to return edge attributes
    :type graph: nx.Graph object

    :param attribute: edge attribute to return
    :type attribute: str

    :return: set of unique attributes for all edges
    :rtype: set
    """
    return set([x[2].get(attribute) for x in graph.edges(
        data=True) if x[2].get(attribute)])


def get_nodes_attribute_set(graph: nx.Graph, attribute: str) -> set:
    """
    Returns the set of selected attribute for nodes in the twin

    :param graph: NetworkX graph object to return node attributes
    :type graph: nx.Graph object

    :param attribute: node attribute to return
    :type attribute: str

    :return: set of unique attributes for all nodes
    :rtype: set
    """
    return set([x[1].get(attribute) for x in graph.nodes(
        data=True) if x[1].get(attribute)])


def ids_by_attribute(graph: nx.Graph, attribute: str,
                     values: list, graph_entity_type: str) -> list:
    """
    Provides subset of either twin edges or nodes based on the attributes
    and list of values provided.


    :param graph: A network X object.
    :type graph: A network X object.
    :param attribute: The attribute to filter the edges.
    :type attribute: str
    :param values:
        A list of values for each edge being found by the function.
    :type values: list
    :param graph_entity_type: A string representing either 'edge' or 'node'.
    :type graph_entity_type: str

    :return: a list of edge or node ids.
    :rtype: list
    """
    if graph_entity_type == 'edge':
        attributes = nx.get_edge_attributes(graph, attribute)
    elif graph_entity_type == 'node':
        attributes = nx.get_node_attributes(graph, attribute)
    else:
        raise TypeError('Not edge or node!')

    return [single_attribute[0]
            for single_attribute in attributes.items()
            if single_attribute[1] in values]


def get_leaf_nodes(graph) -> list:
    """
    Get all leaf nodes for the graph

    :return: ID of the Nodes with only one connection
    :rtype: list
    """
    if graph.is_directed():
        raise NetworkXNotImplemented('Function is ambiguous for directed '
                                     'graph, please us the '
                                     'get_sink_nodes and '
                                     'get_source_nodes functions')
    else:
        return [x for x in graph.nodes() if graph.degree(x) == 1]


def get_source_nodes(graph) -> list:
    """
    Get all source nodes for the graph

    :return: ID of the Nodes with only outward connections
    :rtype: list
    """

    if graph.is_directed():
        return [x for x in graph.nodes() if
                graph.out_degree(x) > 0 and graph.in_degree(x) == 0]
    else:
        raise NetworkXNotImplemented('Function is ambiguous for '
                                     'undirected graph, please us the '
                                     'get_leaf_nodes')


def get_sink_nodes(graph) -> list:
    """
    Get all sink nodes for the graph

    :return: ID of the Nodes with only inwards connections
    :rtype: list
    """

    if graph.is_directed():
        return [x for x in graph.nodes() if
                graph.out_degree(x) == 0 and graph.in_degree(x) > 0]
    else:
        raise NetworkXNotImplemented('Function is ambiguous for '
                                     'undirected graph, please us the '
                                     'get_leaf_nodes')
