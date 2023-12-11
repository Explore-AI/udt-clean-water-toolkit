from typing import Union

import numpy as np
from math import floor
import pandas as pd
from pathlib import Path
from random import randint, seed

try:
    import networkx as nx
except ImportError:
    raise ImportError(
        "The networkx package is required to make use of the graph module. "
        "You can install it using 'conda install -c conda-forge networkx' or "
        "'pip install networkx'."
    )


def save_dataframes_to_excel(dict_of_df: dict, filename: Union[Path, str]):
    """
    Save a dict of dataframes as a single workbook with multiple worksheets

    :param dict_of_df: dict which contains a number of pandas dataframes
    :type dict_of_df: dict of dataframes

    :param filename: a string or Path where to write the file.
        Does not need to include the .xlsx
    :type filename: Path or str
    """

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    if type(filename) is str:
        filename = Path(filename)
    file_path = filename.with_suffix(".xlsx")
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

    # Write each dataframe to a different worksheet.
    for name, df in dict_of_df.items():
        df.to_excel(writer, sheet_name=name)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()


def aggregate_dictionary(d: dict, key: str, agg_func=None) -> float:
    """
    Performed the agg_func on a list of values extracted from a dict
    of dicts where the key of the value matches the key parameter.

    :param d: dict of dicts which contain the values which could be summed.
    :type d: dict of dicts

    :param key: the key of the values to sum
    :type key: Path or str

    example:
        >>> test_data = {'float': {1: 0.001, 2: 2.1, 3: 1000.64},
        >>>      'int': {1: 1, 2: 3, 3: "1000"}}

        >>> aggregate_dictionary(test_data, 1, sum)

        result:
            1.001
    """

    if not agg_func:
        def agg_func(x): return x
    try:
        return agg_func([v for _d in d.values()
                         for k, v in _d.items() if k == key])
    except ValueError:
        return np.NaN


def exponential_decay(x: float, lam: float = 2.0,
                      scale: float = 1000.0, threshold: float = 1e-3) -> float:
    """
    Parameters set specifically for the distance of trunk mains to
    network meters

    :param x: number of meters from the trunk main node to the
        network meters
    :type x: float

    :param lam: a weighting parameter for the relative effect of meters by
        distance. If 1 then all meters are equally weighted, if 2 then every 1
        unit would half the weight of the value.
        defaults 2, so that a network meter 1 km away ~ 60% weighted,
        2 km ~ 30% weighted, 3km ~ 15% weighted
    :type lam: float

    :param scale: a parameter to use for converting the x into generic units
        defaults to 1000 which corresponds to 1km is one unit
    :type scale: float

    :param threshold: set to return empty float if weights is less than
        threshold to reduce sample space
    :type threshold: float

    :return: the exponential decayed value of x
    :rtype: float
    """
    y = np.exp(- lam * x / scale)
    if y > threshold:
        return y
    return float()


def colour_map(x: float,
               colours: list = ['#d0021b', '#f5a623', '#ffea00', '#417505'],
               threshold=1e-8, multiple=1) -> str:
    """
    Used to color html compliant pages, e.g. PowerBI.

    :param x: value to calculate the colours of
    :type x: float

    :param colours: a list of hexadecimal colours to be matched to x.
        Starting with the largest valued one and working down.
    :type colours: list

    :param threshold: a value to subtract from x to allow 3 to be rounded
        down to 2 to ensure compatibility with the original code
    :type threshold: float

    :param multiple: a value to divide x by tp allow for scaling of the
        result to other sequences. e.g. 2 with a list of length 4
        changes the boundary to 0,2,4,6
    :type multiple: list
    """
    index = floor((abs(x / multiple) - threshold))
    if index > len(colours) - 1:
        return colours[0]
    else:
        return colours[::-1][index]


def alarm_to_alert(df: pd.DataFrame, col: str = 'alarm') -> pd.DataFrame:
    if isinstance(df, pd.Series):
        df = pd.DataFrame(df)
        df.columns = [col]
    elif isinstance(df, dict):
        df = pd.DataFrame.from_dict(df, orient='index')
        df.columns = [col]

    df['alert'] = abs(df[col]).fillna(0).replace(np.inf, 0)
    df['rag'] = df['alert'].apply(colour_map)
    df['alert_size'] = (df['alert'] * 10).astype(int) / 10

    return df


def matrix_multiply_dataframes(df1: pd.DataFrame,
                               df2: pd.DataFrame) -> pd.DataFrame:
    """
    Performs matrix multiplication on 2 dataframes
    TODO: should this fail if the index / cols dont match?

    :param df1: first object to multiply
    :type df1: pd.DataFrame

    :param df2: second object to multiply
    :type df2: pd.DataFrame

    :return: the matrix multiplication of the two dataframes
    :rtype: pd.DataFrame
    """

    # only include the union of columns
    interim = set.intersection(set(df1.columns), set(df2.index))
    interim = [i for i in interim]

    w1 = df1[interim].fillna(0).values
    w2 = df2.reindex(index=interim).fillna(0).values

    values = np.matmul(w1, w2)

    return pd.DataFrame(data=values, index=df1.index, columns=df2.columns)


def _flatten(lst: list) -> list:
    """
    Helper function to flatten a list of lists

    :param lst: list of lists to flatten
    :type lst: list

    :return: a list which contains all the lists feed in
    :rtype: list
    """
    out = []
    for i in lst:
        if isinstance(i, list):
            out.extend(i)
        else:
            out.append(i)
    return out


def flatten(l1: Union[list, str, int, float],
            l2: Union[list, str, int, float]) -> list:
    """
    Concatenate two objects into a single list

    :param l1: first object to concatenate
    :type l1: list, str, int or float

    :param l2: second object to concatenate
    :type l2: list, str, int or float

    :return: a list which contains the contents of the lists feed in
    :rtype: list
    """
    if type(l1) != list:
        l1 = [l1]
    if type(l2) != list:
        l2 = [l2]

    return l1 + l2


def less_than(x: float, limit: float = None) -> float:

    if not limit:
        limit = 5000.0

    if 0 < x < limit:
        return x
    return 0.0


def convert_list(x):
    """Returns a list of the input x"""
    if type(x) == list:
        return x
    return [x]


def create_random_subgraph(graph: nx.Graph, number_of_edges: int,
                           local_seed=None) -> nx.Graph:
    if local_seed is not None:
        seed(local_seed)
    start_node = list(graph.nodes)[randint(0, len(graph.nodes))]

    node_list = []
    for n, edge in enumerate(nx.bfs_edges(graph, start_node)):
        if n >= number_of_edges:
            break
        [node_list.append(x) for x in list(edge) if x not in node_list]

    subgraph = graph.subgraph(node_list)
    return subgraph
