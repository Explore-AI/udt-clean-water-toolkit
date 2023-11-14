import matplotlib.pyplot as plt

try:
    import networkx as nx
except ImportError:
    raise ImportError(
        "The networkx package is required to make use of the graph module. "
        "You can install it using 'conda install -c conda-forge networkx' or "
        "'pip install networkx'."
    )


def get_xy(d: dict) -> tuple:
    x, y = None, None

    if 'x' in d:
        x = d['x']
    elif 'SHAPEX' in d:
        x = d['SHAPEX']

    if 'y' in d:
        y = d['y']
    elif 'SHAPEY' in d:
        y = d['SHAPEY']

    if x and y:
        x = round(x, 1)
        y = round(y, 1)
    return x, y


def return_node_positions(graph: nx.Graph, data: str, label: str) -> dict:

    if isinstance(label, list):
        return {n: get_xy(d)
                for n, d in graph.nodes(data=True)
                if (data in d.keys()) and (d[data] in label)}
    else:
        return {n: get_xy(d)
                for n, d in graph.nodes(data=True)
                if (data in d.keys()) and (d[data] == label)}


def chart_nodes(graph: nx.Graph, a: plt.axes,
                label: str, colour: str, data: str = 'layer',
                labels: str = None, node_size: int = 5) -> plt.axes:

    points = return_node_positions(graph, data=data, label=label)
    nx.draw_networkx_nodes(graph,
                           points,
                           nodelist=[i for i in points.keys()],
                           node_size=10,
                           node_color=colour,
                           ax=a,
                           label=label)
    if labels:
        nx.draw_networkx_labels(graph, points, nodesize=node_size,
                                nodelist=[i
                                          for i in points.keys()],
                                labels={n: d
                                        for n, d in graph.nodes(data=labels)
                                        if n in points.keys()},
                                ax=a)
    return a


def chart_edges(graph: nx.Graph, a: plt.axes,
                node_label: str, edge_label: str,
                colour: str, arrowsize: int = 10,
                data: str = 'layer', labels: bool = False) -> plt.axes:

    points = return_node_positions(graph, data=data, label=node_label)
    nodes = list(points.keys())
    edgelist = [(i, j) for i, j, d in graph.edges(nodes, data=data)
                if d == edge_label and all([x in points.keys()
                                            for x in (i, j)])]
    nx.draw_networkx_edges(graph,
                           points,
                           edge_color=colour,
                           ax=a,
                           edgelist=edgelist,
                           arrowsize=arrowsize,
                           label=node_label)

    if labels:
        nx.draw_networkx_labels(graph,
                                points,
                                nodelist=[i for i in points.keys()],
                                labels={i: i for i in points.keys()},
                                ax=a)

    return a


def chart_network(graph: nx.Graph, a: plt.axes = None,
                  labels: bool = False, figsize: tuple = (8, 6)) ->\
        (plt.Figure, plt.Axes):

    if not a:
        f, a = plt.subplots(1, 1, figsize=figsize)

    # chart the nodes
    a = chart_nodes(graph,
                    a,
                    'wNetworkMeter',
                    'b',
                    labels='CONTROLREF' if labels else None,
                    node_size=1)
    a = chart_nodes(graph,
                    a,
                    'wOperationalSite',
                    'r',
                    labels='ASSETNAME' if labels else None)

    # get trunk mains nodes
    a = chart_edges(graph, a, 'trunk_node', 'wTrunkMain', 'black', 3)
    a = chart_edges(graph, a, 'dist_node', 'wDistributionMain', 'grey', 1)

    return f, a


def get_graph_center_coords(graph):
    graph = graph.to_undirected()
    graph = [graph.subgraph(p).copy()
             for p in nx.connected_components(graph)][0]
    center = nx.center(graph)[0]
    details = graph.nodes(data=True)[center]
    center_lon, center_lat = get_xy(details)
    return center_lat, center_lon
