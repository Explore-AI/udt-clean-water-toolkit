import folium

import data_factory.AnalyticalTwin.vis as vis
from data_factory.AnalyticalTwin.chart import get_graph_center_coords
from data_factory.AnalyticalTwin.analytical_twin import CleanTwin
from data_factory.AnalyticalTwin.geospatial import convert_coordinates
from data_factory.AnalyticalTwin.utils import create_random_subgraph


class TestChartModule:
    @classmethod
    def setup(cls):
        twin = CleanTwin(analytical_twin_folder='examples/AnalyticalTwin')
        twin.load_graph()
        twin = create_random_subgraph(twin, 200, 10)
        cls.test_graph = twin

    def test_vis_network(self):
        twin = self.test_graph
        x, y = get_graph_center_coords(twin)

        y, x = convert_coordinates(y, x)

        m = folium.Map(location=[x, y], zoom_start=10)
        for node1, node2 in list(twin.edges):
            vis.add_edge(m, twin, node1, node2)

        for node in list(twin.nodes):
            vis.add_node(m, twin, node, 'black')

    def test_plot_twin(self):
        vis.plot_twin(self.test_graph)
