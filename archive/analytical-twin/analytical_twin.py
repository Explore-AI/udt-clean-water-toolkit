import os
from ast import literal_eval
import datetime
import json
from pathlib import Path, WindowsPath, PosixPath
from data_factory.AnalyticalTwin.twin import convert_edge_geometry

from networkx import Graph, convert, read_gpickle, \
    set_node_attributes, is_empty, set_edge_attributes, DiGraph


def locate_twin(twin_name: str) -> str:
    """
    Function to locate Twin with correct mount based on standard
    environment variable

    :param twin_name: specifies the name of the twin,
     pass either "SmartNetwork" or "SmartWaste"
    :type twin_name: str

    :return: path to twin with correct mount
    :rtype: string
    """
    try:
        product_short = os.environ["PRODUCT_SHORT"].lower()
    except KeyError as E:
        raise Exception(f"Cluster not correctly configured to access "
                        f"Digital Twin, the enviroment variable PRODUCT_SHORT "
                        f"is needed. {E}")

    if twin_name not in ['SmartNetwork', 'SmartWaste']:
        raise ValueError(f'Area must be either "clean" or "waste",'
                         f' value passed: {twin_name}')

    return f"/dbfs/mnt/{product_short}_shared_prd/{twin_name}/AnalyticalTwin"


def date_hook(json_dict: dict) -> dict:
    """
    Converts values of the dict to date format
    if they are in the following str format 'YYYY-MM-DD'.

    :param json_dict: dict which any value in the str format 'YYYY-MM-DD'
        should be converted to date
    :type json_dict: dict

    :return: dict with dates instead of 'YYYY-MM-DD' strings
    :rtype: dict
    """
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = datetime.datetime.fromisoformat(value)
        except (ValueError, TypeError):
            pass
    return json_dict


def validate_twin_filename(filename: str, file_mask: str,
                           file_extension: str = '') -> bool:
    """
    Validate if the name of a file or folder is in the following format
    {file_mask}_YYYYMMDD_HHMMSS{file_extension}

    :param filename: name of the file which needs to be validated
    :type filename: str

    :param file_mask: beginning of the file's name,
        e.g. if files are named like ABC_YYYYMMDD_HHMMSS, pass 'ABC'
    :type file_mask: str

    :param file_extension: extension of the file (with a dot in front),
        e.g '.json', defaults to blank - for folders names
    :type file_extension: str

    :return: True if a filename is valid and False if it's not
    :rtype: bool
    """
    try:
        datetime.datetime.strptime(
            filename, f'{file_mask}_%Y%m%d_%H%M%S{file_extension}')
        return True
    except ValueError:
        return False


class Twin:
    """
    The Twin object extends NetworkX Graph,
    as a default it connects to the
    '/dbfs/mnt/dpsn_shared/SmartNetwork/AnalyticalTwin'
    but a different location can be passed

    :param twin_name: specifies twin_name, either SmartNetwork or SmartWaste
    :type twin_name: str

    :param analytical_twin_folder: path to the twins and layers
    :type analytical_twin_folder: str

    example:

    .. highlight:: python
    .. code-block:: python

        g = Twin()
    """

    def __class__(self):
        return Twin(twin_name=self.twin_name,
                    analytical_twin_folder=self.analytical_twin_folder,
                    pkl_name=self.pkl_name)

    def __init__(self, twin_name: str, analytical_twin_folder: str = None,
                 pkl_name: str = None):
        try:
            self.prefix
        except AttributeError:
            raise Exception('Please use CleanTwin() or WasteTwin()'
                            ' class instead')

        if not analytical_twin_folder:
            self.analytical_twin_folder = Path(locate_twin(twin_name))
        else:
            self.analytical_twin_folder = Path(analytical_twin_folder)

        self.version = None  # version of the twin
        self._set_version = False  # flags if version was set up by user
        # available versions of twin
        self._versions = {x.parts[-2]: datetime.datetime.strptime(
            x.parts[-2], f'{self.prefix}_%Y%m%d_%H%M%S')
            for x in self.analytical_twin_folder.glob('DigitalTwin/*/*')
            if validate_twin_filename(x.parts[-2], self.prefix)
            and x.parts[-1] == self.pkl_name}
        if not self._versions:
            raise Exception(
                f'No twins available in the following location'
                f' \'{self.analytical_twin_folder}\'')
        # available types of layers
        self._layers = {x.parts[-2]: Path(*x.parts[0:-1]) for x in
                        self.analytical_twin_folder.glob('Layers/*/*')
                        if validate_twin_filename(x.parts[-1], x.parts[-2],
                                                  '.json')}
        self._added_layers = {}  # tracking what layers were already added

        super().__init__()

    def __str__(self):
        return f'TW {self.twin_name} Graph - NetworkX Extension'

    def list_digital_twins(self) -> list:
        """
        List all available versions of digital twin in the 'DigitalTwin' folder
        from the path passed while creating a Twin() object,
        if no path was passed twins from the following location will be listed
        '/dbfs/mnt/dpsn_shared/SmartNetwork/AnalyticalTwin/DigitalTwin'

        :return: Returns a list of all available versions of digital twin
        :rtype: list
        """
        return list(self._versions.keys())

    def set_version(self, version: str):
        """
        Method to set a version of the twin for other methods of the class.
        If the version is not set, other methods will use
        the latest available data.

        :param version: Folder which contains the digital twin,
            e.g. CW_20201008_060004
        :type version: str
        """
        if version in self._versions.keys():
            self.version = version
            self._set_version = True
        else:
            raise Exception(f'Version not found: {version}')

    def load_graph(self, version: str = None):
        """
        Load twin from the folder chose in a set_version method,
        or load the latest version of the twin if the version wasn't set

        Edge geometries are converted from WKT to shapely.geometry if necessary

        :param version: Folder which contains the digital twin,
            e.g. CW_20201008_060004
        :type version: str
        """
        if version:
            self.set_version(version)
        if self.version is None:
            self.version = max(self._versions, key=self._versions.get)
            print(f'loading the latest version of the twin - {self.version},'
                  f' if you need different version use .set_version method'
                  f' first and load_graph again')

        incoming_graph_data = read_gpickle(self.analytical_twin_folder /
                                           'DigitalTwin' / self.version /
                                           self.pkl_name)
        # convert edge geometries from WKT to shapely.geometry objects
        incoming_graph_data = convert_edge_geometry(
            incoming_graph_data, wkt_to_geom=True)

        convert.to_networkx_graph(incoming_graph_data, create_using=self)
        self._added_layers = {}
        print(f'{self.version} version of the twin loaded')

    def list_layers(self) -> list:
        """
        List all available layers in a 'Layers' folder
        from the path passed while creating a Twin() object,
        if no path was passed lists layers from the following location
        '/dbfs/mnt/shared_prd/SmartNetwork/AnalyticalTwin/Layers'
        or for waste
        '/dbfs/mnt/shared_prd/SmartWaste/AnalyticalTwin/Layers'

        :return: Returns list of all available layers
        :rtype: list
        """
        return list(self._layers.keys())

    def list_layer_versions(self, *args: str) -> dict:
        """
        List all available versions for the passed layers.
        An exception is raised if any layer is not available.

        :param args: Layers for which versions will be listed
        :type args: str

        :return: Returns dict with the layers as keys and their versions
            as values
        :rtype: dict
        """

        # checks if passed layers are available and raises an exception if not
        layers = list(self._layers.keys())
        if not set(args).issubset(layers):
            raise Exception(f'Layer(s) not found:'
                            f' {set(args).difference(layers)}')

        if not args:
            args = list(self._layers.keys())

        # for each layer adds an item to a dictionary
        layer_versions = {}
        for layer in args:
            layer_path = Path(self._layers[layer])
            all_jsons = layer_path.glob('**/*.json')
            layer_versions[layer] = [x.name
                                     for x in all_jsons if layer in x.name]
        return layer_versions

    def add_layer_from_dict(self, layer_dict: dict, reference: str,
                            version_of_data: str = None):
        """
        Add layer to the digital twin from the passed python dictionary.

        :param layer_dict: a dictionary containing layer data, must be
            structured as a dictionary with 3 keys - "node", "edge" and
            "edge_key", their values must be another dictionaries with keys
            which are the nodes or an attribute (eg GISID) of the edges
            accordingly, for example:

            .. highlight:: python
            .. code-block:: python

                {"node": {"1718223": {"test_attribute_node1": 2000},
                        "1765746": {"test_attribute_node1": 55,
                                    "test_attribute_node2": 66}},
                "edge": {"1112210": {"test_attribute": 2000}},
                "edge_key": "GISID"
                }

        :type layer_dict: dict

        :param reference: name which will be used in the twin
        :type reference: str

        :param version_of_data: Optional, this value will be stored in
            a dictionary with added layers, to prevent adding the same version
            of the layer twice. Defaults to the concatenation of 'dict: ' and
            memory address of the dictionary
        :type version_of_data: str
        """

        # check if twin data was already loaded
        if is_empty(self):
            raise Exception('The graph is empty. Load twin data first.')

        if type(layer_dict) != dict:
            raise TypeError(f'\'layer\' should be a dictionary'
                            f' not {type(layer_dict)}')

        # validate structure of the data
        if not {'node', 'edge', 'edge_key'}.issubset(layer_dict.keys()):
            raise Exception('The dictionary must contain the following keys:'
                            ' \'node\', \'edge\' and \'edge_key\'')

        if not version_of_data:
            version_of_data = f'dict: {id(layer_dict)}'

        # checks if this version of the layer was already added to the graph
        if version_of_data in self._added_layers.keys():
            raise Exception(
                f'Data from {version_of_data} was already added to the graph'
                f' with \'{self._added_layers[version_of_data]}\' reference')

        # checks if the reference was already added to the graph
        if reference in self._added_layers.values():
            version_of_data = [k for k, v in self._added_layers.items()
                               if v == reference][0]
            raise Exception(f'\'{reference}\' reference was already used'
                            f' for data from {version_of_data}')

        # convert keys to tuples from strings
        # (nodes for the waste twin are tuples)
        if self.prefix == 'WW':
            layer_dict['node'] = {literal_eval(k): v
                                  for k, v in layer_dict['node'].items()}

        # edges ids are tuples for clean and waste,
        # convert them to tuples from strings
        # in case if attributes are being added by edges ids
        if layer_dict['edge_key'] == '':
            edge_attributes = {literal_eval(k): v
                               for k, v in layer_dict['edge'].items()}
        else:
            edge_attributes = self.get_node_ids(layer_dict['edge'],
                                                layer_dict['edge_key'])

        set_node_attributes(self, layer_dict['node'], reference)
        set_edge_attributes(self, edge_attributes, reference)
        self._added_layers[version_of_data] = reference
        print(f'Layer added as \'{reference}\' using data'
              f' from {version_of_data}')

    def add_layer_from_path(self, layer_path: str, reference: str,
                            version_of_data: str = None):
        """
        Add layer to the digital twin from the specific path.

        :param layer_path: path to the json file containing data for the layer
        :type layer_path: str

        :param reference: name which will be used in the twin
        :type reference: str

        :param version_of_data: Optional, this value will be stored in
            a dictionary with added layers, to prevent adding the same version
            of the layer twice. Defaults to the value passed as layer_path
        :type version_of_data: str
        """

        if type(layer_path) != str and type(layer_path) != WindowsPath\
                and type(layer_path) != PosixPath:
            raise TypeError(f'\'layer\' should be string or os.PathLike object'
                            f' not {type(layer_path)}')

        # validates path, and checks if it's a json format
        layer_path = Path(layer_path)

        if not layer_path.is_file():
            raise Exception(f'{layer_path} path is not valid')

        if layer_path.parts[-1][-5:] != '.json':
            raise Exception('Format of the file is not valid,'
                            ' it should be in json format.')

        if not version_of_data:
            version_of_data = layer_path

        # saving layer data as loaded_dict
        with open(layer_path) as dumped_dict:
            loaded_dict = json.load(dumped_dict, object_hook=date_hook)

        self.add_layer_from_dict(loaded_dict, reference=reference,
                                 version_of_data=version_of_data)

    def add_layer(self, layer: str, layer_version: str = None,
                  reference: str = None):
        """
        Add layer to the digital twin.
        Optionally specify version of the layer to add and its reference
        to use in the graph. Defaults reference to the value
        of the layer parameter. And defaults layer_version as follows:
        - latest available layer if version of the graph wasn't set by user
        - otherwise, nearest layer version after the selected twin version,
        or latest available layer if no layer versions after the twin version
        are available

        An exception is raised, if the layer is not available.

        :param layer: Name of the folder with the layer data
            e.g "Acoustic_Loggers"
        :type layer: str

        :param layer_version: Optional, version of the file containing
            layer data, in the following format "YYYYMMDD_HHMMSS"
        :type layer_version: str

        :param reference: Optional, name which will be used in the twin.
            Defaults to the same value as passed as the layer parameter
            (e.g. "Acoustic_Loggers"),
            unless this type of layer was already added to the graph
            then defaults to layer name suffixed with version's datetime
            (e.g. "Acoustic_Loggers_20200101_060000")
        :type reference: str
        """

        # check if there are any layers in the location
        if not self._layers:
            raise Exception(f'No layers available in the following'
                            f' location \'{self.analytical_twin_folder}\'')

        # check if passed layer is available
        if layer not in self._layers:
            raise Exception(f'Layer not found: {layer}')

        # sets up data_version - name of the file with required
        # version of the layer
        if layer_version is not None:
            data_version = f'{layer}_{layer_version}.json'
            if data_version not in self.list_layer_versions(layer)[layer]:
                raise Exception(f'Version of {layer} layer not found:'
                                f' {layer_version}')
        else:
            layer_versions = self.list_layer_versions(layer)
            latest_layer = []

            # if version of the twin was set up by user
            if self._set_version:
                # date of the loaded twin
                twin_version_dt = self._versions[self.version]
                # list of layers available after the twin's date
                latest_layer = [x for x in layer_versions[layer]
                                if datetime.datetime.strptime(
                        x, f'{layer}_%Y%m%d_%H%M%S.json')
                                >= twin_version_dt]
                # if there are layers after this date,
                # finds the closest one
                if latest_layer:
                    data_version = min(
                        latest_layer,
                        key=lambda x: datetime.datetime.strptime(
                            x, f'{layer}_%Y%m%d_%H%M%S.json'))

            # if version of the graph wasn't set by user or no layers
            # were found after date of the twin,
            # finds the latest available version of the layer
            if not self._set_version or not latest_layer:
                data_version = max(
                    [x for x in layer_versions[layer]],
                    key=lambda x: datetime.datetime.strptime(
                        x, f'{layer}_%Y%m%d_%H%M%S.json'))

        # set up reference if it wasn't specified
        # if this type of layer was already added to the graph
        # will use full name with date
        # otherwise short name without date
        if reference is None:
            added_layers = [x for x in self._added_layers.keys()
                            if layer in x]
            if added_layers:
                reference = data_version.replace('.json', '')
            else:
                reference = layer

        # setting up path to the layer
        layer_path = Path(self._layers[layer], data_version)

        self.add_layer_from_path(layer_path, reference,
                                 version_of_data=data_version)

    def add_layers(self, *args: str):
        """
        Add passed layers to the digital twin,
        takes name of the layer's folder,
        e.g. Acoustic_Loggers
        An exception is raised, if any of passed layers are not available.

        :param args: layers to add to the twin
        :type args: str
        """
        all_layers = self.list_layers()
        if not set(args).issubset(all_layers):
            raise Exception(f'Layer(s) not found:'
                            f' {set(args).difference(all_layers)}')

        for layer in args:
            self.add_layer(layer)

    def added_layers(self) -> dict:
        """
        Returns dict with source files and references of the layers which were
        added to the graph.

        :return: Dictionary with the layers which were added to the graph,
            e.g. {'Acoustic_Loggers_20210206_080000.json': 'AL',
            'Acoustic_Loggers_20210209_080000.json': 'AL2'}
        :rtype: dict
        """
        return self._added_layers

    def get_node_ids(self, gisid_edge_attributes: dict,
                     attribute_key: str = 'GISID') -> dict:
        """
        Converts the gisid keyed data into node pairs based on the version of
        the twin loaded into memory.

        :param gisid_edge_attributes: gisid keyed data to be added to the graph
        :type gisid_edge_attributes: dict

        :param attribute_key: key in the edges attributes to use for finding
            the nodes
        :type attribute_key: str

        :return: Dictionary of node pairs to be added to the graph
        :rtype: dict
        """
        edge_attributes = {}
        missing_edges = []
        for key, value in gisid_edge_attributes.items():
            try:
                edge_attributes.update(
                    {(edge_data[0], edge_data[1]): value
                     for edge_data in self.edges(data=True)
                     if edge_data[2][attribute_key] == int(key)})
            except Exception:
                missing_edges.append(int(key))

        if len(missing_edges) != 0:
            print(f'Missing gisids: {missing_edges}')
        return edge_attributes


class CleanTwin(Twin, Graph):
    """
    One of the Twin object extends NetworkX Graph which provides the interface
    for the clean waster twin. As a default it connects to the
    /dbfs/mnt/dpsn_shared_prd/SmartNetwork/AnalyticalTwin

    :param analytical_twin_folder: path to the twins and layers
    :type analytical_twin_folder: str

    example:

    .. highlight:: python
    .. code-block:: python

        g = CleanTwin()
    """

    def __init__(self, analytical_twin_folder: str = None,
                 pkl_name: str = None):
        self.twin_name = 'SmartNetwork'
        self.pkl_name = 'thames_water.pkl' if not pkl_name else pkl_name
        self.prefix = 'CW'
        super().__init__(twin_name=self.twin_name,
                         analytical_twin_folder=analytical_twin_folder,
                         pkl_name=self.pkl_name)

    def __repr__(self):
        return f'CleanTwin(\'{self.analytical_twin_folder}\')'

    def __class__(self):
        return CleanTwin(analytical_twin_folder=self.analytical_twin_folder,
                         pkl_name=self.pkl_name)


class WasteTwin(Twin, DiGraph):
    """
    One of the Twin object extends NetworkX Graph which provides the interface
    for the waste twin. As a default it connects to the
    /dbfs/mnt/dpsn_shared_prd/SmartWaste/AnalyticalTwin

    :param analytical_twin_folder: path to the twins and layers
    :type analytical_twin_folder: str

    example:

    .. highlight:: python
    .. code-block:: python

        g = WasteTwin()
    """

    def __init__(self, analytical_twin_folder: str = None,
                 pkl_name: str = None):
        self.twin_name = 'SmartWaste'
        self.pkl_name = 'thames_waste.pkl' if not pkl_name else pkl_name
        self.prefix = 'WW'
        super().__init__(twin_name=self.twin_name,
                         analytical_twin_folder=analytical_twin_folder,
                         pkl_name=self.pkl_name)

    def __repr__(self):
        return f'WasteTwin(\'{self.analytical_twin_folder}\')'

    def __class__(self):
        return WasteTwin(analytical_twin_folder=self.analytical_twin_folder,
                         pkl_name=self.pkl_name)
