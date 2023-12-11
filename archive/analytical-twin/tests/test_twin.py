import networkx as nx
from pathlib import Path

from networkx import NetworkXNotImplemented

import data_factory.AnalyticalTwin.twin as twin


class TestTwinModule:
    @classmethod
    def setup(cls):
        g = twin.get_graph("oxleas_wood_system.pkl", "examples")
        cls.test_graph = g
        g_ww = twin.get_graph("henley.pkl", "examples")
        cls.test_graph_ww = g_ww

    def test_get_graph(self):
        temp_file_name = "tmp/nx_graph.pkl"
        nx.write_gpickle(nx.Graph(), temp_file_name)

        g1 = twin.get_graph("nx_graph.pkl", "tmp")
        outcome = isinstance(g1, nx.Graph)
        assert outcome

    def test_save_graph(self):
        folder = Path("tmp/output")

        folder1, file_name = twin.save_graph(nx.Graph(),
                                             "test.pkl",
                                             folder)
        assert (folder/"test.pkl").exists()
        assert "tmp/output" == folder1
        assert "test.pkl" == file_name

        folder1, file_name = twin.save_graph(nx.Graph(),
                                             "test2.pkl",
                                             str(folder))
        assert (folder/"test2.pkl").exists()
        assert "tmp/output" == folder1
        assert "test2.pkl" == file_name

    def test_summarize_graph(self):
        result = twin.summarise_graph(self.test_graph)
        assert 'wTrunkMain' in result
        assert result['wTrunkMain'] == 4644
        assert result['dist_node'] == 2548

    def test_summarize_graphs(self):
        result = twin.summarise_graphs({'twin': self.test_graph})
        assert 'twin' in result

    def test_convert_edge_geometry(self):
        g = twin.convert_edge_geometry(self.test_graph_ww, geom_to_wkt=True)
        test_string = g.edges[(475774.3, 182058.2),
                              (475767.9, 182061.5)]['geometry'][:18]
        assert test_string == 'LINESTRING (475774'

        g2 = twin.convert_edge_geometry(g, wkt_to_geom=True)
        geometry = g2.edges[(475774.3, 182058.2),
                            (475767.9, 182061.5)]['geometry']
        assert str(geometry) == 'LINESTRING (475774.3 182058.2, ' \
                                '475767.9 182061.5)'

        try:
            g = twin.convert_edge_geometry('g', wkt_to_geom=True)
        except TypeError as E:
            assert str(E) == 'The provided graph was not a networkx graph ' \
                             'and was not modified.'

        try:
            g = twin.convert_edge_geometry('g')
        except Exception as E:
            assert str(E) == 'Please choose either geom_to_wkt=True, ' \
                             'or wkt_to_geom=True'

        try:
            g = twin.convert_edge_geometry('g', wkt_to_geom=True,
                                           geom_to_wkt=True)
        except Exception as E:
            assert str(E) == 'Please choose either geom_to_wkt=True, ' \
                             'or wkt_to_geom=True, and not both'

    def test_get_edges_attribute_set(self):
        attribute_set = twin.get_edges_attribute_set(self.test_graph,
                                                     'MATERIAL')
        assert attribute_set == {'BP', 'CI', 'CS', 'DI', 'HPP', 'HPPE',
                                 'MDPE', 'None', 'POL', 'ST', 'UNK', 'UPC'}

    def test_get_nodes_attribute_set(self):
        attribute_set = twin.get_nodes_attribute_set(self.test_graph,
                                                     'VALVEGROUP')
        assert attribute_set == {'DBV', 'DPV', 'EV', 'GP', 'PBV', 'SSV', 'ZBV'}

    def test_leaf_nodes(self):
        assert len(twin.get_leaf_nodes(self.test_graph)) == 3432
        try:
            assert len(twin.get_leaf_nodes(self.test_graph_ww)) == 0
        except NetworkXNotImplemented:
            assert True

    def test_sink_nodes(self):
        assert len(twin.get_sink_nodes(self.test_graph_ww)) == 168
        try:
            assert len(twin.get_sink_nodes(self.test_graph)) == 0
        except NetworkXNotImplemented:
            assert True

    def test_source_nodes(self):
        assert len(twin.get_source_nodes(self.test_graph_ww)) == 533
        try:
            assert len(twin.get_source_nodes(self.test_graph)) == 0
        except NetworkXNotImplemented:
            assert True

    def test_ids_by_attribute(self):
        edges = twin.ids_by_attribute(self.test_graph, 'Shape_Leng',
                                      [15.0999353598], 'edge')
        assert edges == [('1796018', '10002112')]

        nodes = twin.ids_by_attribute(self.test_graph, 'layer',
                                      ['wNetworkOptValve'], 'node')
        assert len(nodes) == 4847
