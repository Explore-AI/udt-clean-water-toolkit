import datetime
import json
from pathlib import Path
import os


def validate_dict(layer_dict: dict):
    """
    Checks if passed dictionary contains 3 main keys 'node', 'edge'
    and 'edge_key', and if value of the 'edge_key' key is string

    :param layer_dict: a dictionary which format should be validated
    :type layer_dict: dict

    :return: Returns True if the dictionary is in a required format,
        otherwise returns False
    :rtype: bool
    """
    # check type
    if type(layer_dict) != dict:
        raise Exception(f'It should be a python dictionary,'
                        f' not {type(layer_dict)}')

    # validate structure of the dictionary
    missing_keys = {'node', 'edge', 'edge_key'}.difference(layer_dict.keys())
    if missing_keys:
        raise Exception(f'The dictionary is missing the following'
                        f' key(s) {missing_keys}')

    # value of the edge_key must be a string
    if type(layer_dict['edge_key']) != str:
        raise Exception(f'Value of the \'edge_key\' key should be string,'
                        f' not {type(layer_dict)}')

    return True


def json_date_converter(o):
    """
    This function is used during the export (as an argument in json.dump),
    if a dictionary contains a datetime object it will be converted to string

    :param o: an object which type would be change from datetime to string
    """
    if isinstance(o, datetime.datetime):
        return o.__str__()


def export_json(layer_dict: dict, layer_name: str, actual_datetime: datetime,
                path: str):
    """
    Export a dictionary to a json file. As default saves file in
    /dbfs/mnt/dpsn_shared/SmartNetwork/AnalyticalTwin/Layers
    but it can be overwritten using a path argument.

    :param layer_dict: a dictionary containing layer data,
        must be structure as dictionary with 3 keys - "node", "edge"
        and "edge_key", their values are another dictionaries with keys which
        are the nodes or an attribute (eg GISID) of the edges accordingly,
        for example:

        .. highlight:: python
        .. code-block:: python

            {"node": {"1718223": {"test_attribute_node1": 2000},
                    "1765746": {"test_attribute_node1": 55,
                                "test_attribute_node2": 66}},
            "edge": {"1112210": {"test_attribute": 2000}},
            "edge_key": "GISID"
            }

    :type layer_dict: dict

    :param layer_name: name of the layer, the output file will be saved
        in a folder called layer_name and json file will be called
        layer_name_YYYYMMDD_HHMMSS.json
    :type layer_name: str

    :param actual_datetime: datetime of the source data
    :type actual_datetime: datetime

    :param path: Specify path to dump json file to
    :type path: str
    """
    validate_dict(layer_dict)

    path = Path(path)

    if path.parts[-1] != 'Layers':
        path = path / 'Layers'

    path = path / layer_name

    if not path.exists():
        os.makedirs(path)

    actual_datetime = actual_datetime.strftime('%Y%m%d_%H%M%S')
    path = path / f'{layer_name}_{actual_datetime}.json'

    with open(path, 'w') as outfile:
        json.dump(layer_dict, outfile, default=json_date_converter)
