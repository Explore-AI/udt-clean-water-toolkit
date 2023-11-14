import data_factory.AnalyticalTwin.chart as chart
import data_factory.AnalyticalTwin.twin as twin
import matplotlib.pyplot as plt


class TestChartModule:
    @classmethod
    def setup(cls):
        g = twin.get_graph("oxleas_wood_system.pkl", "examples")
        cls.test_graph = g

    def test_chart_network(self):
        f, a = chart.chart_network(self.test_graph)
        assert isinstance(f, plt.Figure)
        assert isinstance(a, plt.Axes)
