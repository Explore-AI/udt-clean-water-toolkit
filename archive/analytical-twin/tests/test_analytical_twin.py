import networkx as nx

from data_factory.AnalyticalTwin.analytical_twin import CleanTwin, WasteTwin
import datetime
from pathlib import Path


class TestAnalyticalTwinModule:
    @classmethod
    def setup(cls):
        cls.twin = CleanTwin(analytical_twin_folder='examples/AnalyticalTwin')
        cls.twin_ww = WasteTwin(
            analytical_twin_folder='examples/AnalyticalTwin_WW')

    def test_versions(self):
        versions = self.twin.list_digital_twins()

        assert len(versions) == 5
        assert 'CW_20201008_060004' in versions

    def test_load_default(self):
        self.twin.load_graph()

        assert self.twin.number_of_nodes() == 24447
        assert\
            self.twin.edges['7482125', '7482091|7561557|7570922']['layer'] ==\
            'wDistributionMain'
        assert self.twin.number_of_edges() == 25985

    def test_load_version(self):
        self.twin.set_version('CW_20201008_060004')
        self.twin.load_graph()

        assert self.twin.number_of_nodes() == 24397
        assert self.twin.number_of_edges() == 25933

    def test_load_graph(self):
        self.twin.load_graph('CW_20201008_060004')

        assert self.twin.number_of_nodes() == 24397
        assert self.twin.number_of_edges() == 25933

    def test_load_waste_graph(self):
        self.twin_ww.load_graph()

        assert self.twin_ww.number_of_nodes() == 2222
        assert self.twin_ww.number_of_edges() == 2312

    def test_set_version(self):
        try:
            self.twin.set_version('CW_20201008')
        except Exception as E:
            assert str(E) == 'Version not found: CW_20201008'

    def test_layers(self):
        layers = self.twin.list_layers()

        assert len(layers) == 2
        assert 'Acoustic_Loggers' in layers

    def test_layer_versions(self):
        al_versions = self.twin.list_layer_versions('Acoustic_Loggers')

        assert isinstance(al_versions, dict)
        assert len(al_versions['Acoustic_Loggers']) == 4

        try:
            self.twin.list_layer_versions('Acoustic_Loggers',
                                          'not existing layer')
        except Exception as E:
            assert str(E) == 'Layer(s) not found: {\'not existing layer\'}'

    def test_add_layer_latest_twin(self):
        # without loading twin first
        try:
            self.twin.add_layer('Acoustic_Loggers')
        except Exception as E:
            assert str(E) == 'The graph is empty. Load twin data first.'

        self.twin.load_graph()

        # not existing layer
        try:
            self.twin.add_layer('not_existing_layer')
        except Exception as E:
            assert str(E) == 'Layer not found: not_existing_layer'

        # not existing version
        try:
            self.twin.add_layer('Acoustic_Loggers',
                                'not_existing_version', 'AL')
        except Exception as E:
            assert str(E) == 'Version of Acoustic_Loggers layer not found:' \
                             ' not_existing_version'

        self.twin.add_layer('Acoustic_Loggers', '20210206_080000', 'AL')
        assert self.twin.nodes(data=True)['1718223']['AL'] ==\
            {'start_date': datetime.datetime(2017, 8, 10, 15, 0),
             'end_date': datetime.datetime(2021, 4, 8, 3, 30)}

        # testing adding attributes to the edges
        for n1, n2, d in self.twin.edges(data=True):
            if d['GISID'] == 7482091:
                edge_attrb = d['AL']
                break
        assert edge_attrb == {"test_attribute": 2000}

        # trying to add the same layer again
        try:
            self.twin.add_layer('Acoustic_Loggers', '20210206_080000', 'AL')
        except Exception as E:
            assert str(E) == 'Data from Acoustic_Loggers_20210206_080000.json'\
                             ' was already added to the graph' \
                             ' with \'AL\' reference'

    def test_add_layer_from_dict(self):
        layer_dict = {"node": {"1718223": {"start_date": "2018-05-03 11:54:00",
                                           "end_date": "2021-04-08 03:30:00"}},
                      "edge": {"1112210": {"test_attribute": 2000}},
                      "edge_key": "GISID"
                      }
        self.twin.load_graph()
        self.twin.add_layer_from_dict(layer_dict, 'AL from dict')

        assert self.twin.nodes(data=True)['1718223']['AL from dict'] ==\
               {'end_date': '2021-04-08 03:30:00',
                'start_date': '2018-05-03 11:54:00'}

        # trying to load the same dict twice
        try:
            self.twin.add_layer_from_dict(layer_dict, 'AL from dict')
        except Exception as E:
            assert str(E) == f'Data from dict: {id(layer_dict)} was already' \
                             f' added to the graph with \'AL from dict\'' \
                             f' reference'

        # not valid dict
        layer_dict = {"node": {"1718223": {"start_date": "2018-05-03 11:54:00",
                                           "end_date": "2021-04-08 03:30:00"}},
                      "edges": {"1112210": {"test_attribute": 2000}}}
        try:
            self.twin.add_layer_from_dict(layer_dict, 'AL from dict2')
        except Exception as E:
            assert str(E) == 'The dictionary must contain the following' \
                             ' keys: \'node\', \'edge\' and \'edge_key\''

        # passing wrong type of data
        try:
            self.twin.add_layer_from_dict('some string', 'AL from dict2')
        except Exception as E:
            assert str(E) == '\'layer\' should be a dictionary'\
                             ' not <class \'str\'>'

    def test_add_layer_from_path(self):
        path = 'examples/AnalyticalTwin/Layers/Acoustic_Loggers/' \
               'Acoustic_Loggers_20210209_080000.json'
        self.twin.load_graph()
        self.twin.add_layer_from_path(path, 'AL from path')

        assert self.twin.nodes(data=True)['1718223']['AL from path'] ==\
               {'end_date': datetime.datetime(2021, 4, 8, 3, 30),
                'start_date': datetime.datetime(2018, 5, 3, 11, 54)}

        # trying to load data from the same path
        try:
            self.twin.add_layer_from_path(path, 'AL from path2')
        except Exception as E:
            assert str(E) == f'Data from {Path(path)} was' \
                             f' already added to the graph with' \
                             f' \'AL from path\' reference'

        # passing wrong type of data
        try:
            self.twin.add_layer_from_path(22, 'AL from path2')
        except Exception as E:
            assert str(E) == '\'layer\' should be string or os.PathLike' \
                             ' object not <class \'int\'>'

        # not valid path
        path = 'not_existing_path/Acoustic_Loggers_20210209_080000.json'
        try:
            self.twin.add_layer_from_path(path, 'AL')
        except Exception as E:
            assert str(E) == f'{Path(path)} path is not valid'

        # valid path, but not json
        path = 'examples/AnalyticalTwin/DigitalTwin/CW_20201008_060004/' \
               'thames_water.pkl'
        try:
            self.twin.add_layer_from_path(path, 'AL')
        except Exception as E:
            assert str(E) == 'Format of the file is not valid,'\
                             ' it should be in json format.'

    def test_added_layers(self):
        self.twin.load_graph()
        self.twin.add_layer('Acoustic_Loggers', '20210206_080000', 'AL')
        self.twin.add_layer('Acoustic_Loggers', '20210209_080000', 'AL2')
        self.twin.add_layer('Acoustic_Loggers', '20210209_080300', 'AL3')
        added_layers_dict = self.twin.added_layers()

        assert len(added_layers_dict) == 3
        assert\
            self.twin.added_layers()['Acoustic_Loggers_20210209_080000.json']\
            == 'AL2'

        self.twin.load_graph()
        assert self.twin.added_layers() == {}

    def test_add_layer_set_twin(self):
        self.twin.set_version('CW_20210208_060001')
        self.twin.load_graph()

        # adding a layer with default version and reference
        self.twin.add_layer('Acoustic_Loggers')
        assert self.twin.nodes(data=True)['1718223']['Acoustic_Loggers'] == \
            {'end_date': datetime.datetime(2021, 4, 8, 3, 30),
             'start_date': datetime.datetime(2018, 5, 3, 11, 54)}
        assert\
            self.twin.added_layers()['Acoustic_Loggers_20210209_080000.json']\
            == 'Acoustic_Loggers'

    def test_add_layers(self):
        self.twin.set_version('CW_20210208_060001')
        self.twin.load_graph()
        self.twin.add_layers('Acoustic_Loggers', 'Acoustic_Loggers_test')

        assert self.twin.added_layers() ==\
            {'Acoustic_Loggers_20210209_080000.json':
             'Acoustic_Loggers',
             'Acoustic_Loggers_test_20210209_080000.json':
             'Acoustic_Loggers_test'}
        assert self.twin.nodes(data=True)['1718223']['Acoustic_Loggers'] == \
            {'end_date': datetime.datetime(2021, 4, 8, 3, 30),
             'start_date': datetime.datetime(2018, 5, 3, 11, 54)}

        self.twin.load_graph()
        try:
            self.twin.add_layers('Acoustic_Loggers', 'not_existing_layer1')
        except Exception as E:
            assert str(E) == 'Layer(s) not found: {\'not_existing_layer1\'}'

    def test_versions_ww(self):
        versions = self.twin_ww.list_digital_twins()

        assert len(versions) == 2
        assert 'WW_20201008_060004' in versions

    def test_layer_versions_ww(self):
        al_versions = self.twin.list_layer_versions('Acoustic_Loggers')

        assert isinstance(al_versions, dict)
        assert len(al_versions['Acoustic_Loggers']) == 4

        try:
            self.twin.list_layer_versions('Acoustic_Loggers',
                                          'not existing layer')
        except Exception as E:
            assert str(E) == 'Layer(s) not found: {\'not existing layer\'}'

    def test_subgraph(self):
        self.twin.load_graph()
        self.twin.edge_subgraph([(x[0], x[1])
                                 for x in self.twin.edges(data=True)])

    def test_direction(self):
        assert nx.is_directed(self.twin) is False
        assert nx.is_directed(self.twin_ww) is True
