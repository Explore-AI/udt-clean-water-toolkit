from pytest import approx
import pandas as pd
import datetime
from pathlib import Path
import numpy as np
from networkx import Graph, is_connected

import data_factory.AnalyticalTwin.utils as utils
import data_factory.AnalyticalTwin.twin as twin


class TestUtilsModule:
    sample_data = {'string': ['value 1', 'value 2', 'value 3'],
                   'integer': [1, 5000, 10000],
                   'float': [0.001, 2.1, 1000.64],
                   'date_time': [np.datetime64(datetime.date.today()),
                                 np.datetime64(datetime.date.today()),
                                 np.datetime64(datetime.date.today())]
                   }

    sample_data_frame = pd.DataFrame(sample_data)
    testing_folder = Path("tmp")

    def test_save_dataframes_to_excel(self):
        path = self.testing_folder/"sample_data_frame"
        dict_to_save = {"test1": self.sample_data_frame,
                        "test2": self.sample_data_frame,
                        "test3": self.sample_data_frame}

        utils.save_dataframes_to_excel(dict_to_save, path)

        reading = {}
        for x in ["test1", "test2", "test3"]:
            reading[x] = pd.read_excel(path.with_suffix(".xlsx"),
                                       sheet_name=x,
                                       index_col=0)

        for layer in reading.keys():
            dataframe = reading[layer]
            for column in dataframe:
                assert reading[layer][column].name == \
                       dict_to_save[layer][column].name
                for index in range(len(reading[layer][column].values)):
                    assert reading[layer][column].values[index] == \
                           dict_to_save[layer][column].values[index]

    def test_aggregate_dictionary(self):
        test_data = {'float': {"1": 0.001, "2": 2.1, "3": 1000.64},
                     'int': {"1": 1, "2": 3, "3": "1000"}}

        # Testing no aggregation function
        result = utils.aggregate_dictionary(test_data, "1")
        assert result == [0.001, 1]

        # Testing sum aggregation function
        result = utils.aggregate_dictionary(test_data, "2", sum)
        assert result == 5.1

        # Testing value error
        # TODO add error check for this with the help of Aidan
        # result = utils.aggregate_dictionary(test_data, 3, int)
        # self.assertEqual(result, 5.1)

    def test_convert_list(self):
        original = self.sample_data['string'][0]

        converted = utils.convert_list(original)
        unconverted = utils.convert_list([original])

        assert type(converted) == list
        assert type(unconverted) == list
        assert original == converted[0]

    def test_less_than(self):
        original = self.sample_data['integer']

        for x in original:
            if x < 5000:
                assert utils.less_than(x) == x
            else:
                assert utils.less_than(x) == 0

        for x in original:
            if x < 8000:
                assert utils.less_than(x, 8000) == x
            else:
                assert utils.less_than(x, 8000) == 0

    def test_colour_map(self):
        # testing base functionality
        assert utils.colour_map(4) == '#d0021b'
        assert utils.colour_map(-3) == '#f5a623'
        assert utils.colour_map(2) == '#ffea00'
        assert utils.colour_map(0.2) == '#417505'

        # Testing the additional parameters which can be used
        assert utils.colour_map(0.9, multiple=1 / 3) == '#f5a623'
        assert utils.colour_map(3, ['#d0021b', '#45b623',
                                    '#ffea00', '#417505']) == \
            '#45b623'

    def test_exponential_decay(self):
        assert utils.exponential_decay(4) == approx(0.9920319)
        assert utils.exponential_decay(5000) == 0.0
        assert utils.exponential_decay(1000, 5) == approx(0.00673794, 3)
        assert utils.exponential_decay(4, 1) == approx(0.996007989)

    def test_matrix_multiply_dataframes(self):
        sample_matrix = {0: [1, 5000, 120],
                         1: [0.1, 2, 100],
                         2: [0.5, 5, 150], }

        sample_matrix_data_frame = pd.DataFrame(sample_matrix)
        x = utils.matrix_multiply_dataframes(sample_matrix_data_frame,
                                             sample_matrix_data_frame)

        result = {0: [561.0, 15600, 518120],
                  1: [50.3, 1004, 15212],
                  2: [76.0, 3260, 23060], }

        result_data_frame = pd.DataFrame(result)

        assert result_data_frame.equals(x)

    def test_flatten(self):
        result = utils.flatten(self.sample_data["integer"],
                               self.sample_data["float"])
        assert result == [1, 5000, 10000, 0.001, 2.1, 1000.64]

        result = utils.flatten(1, 2.1)
        assert result == [1, 2.1]

        result = utils._flatten([[1], 2])
        assert result == [1, 2]

    def test_alarm_to_alert(self):
        # Testing with pandas dataframe
        alert = utils.alarm_to_alert(self.sample_data_frame, "float")

        results = {"alert": [0.001, 2.100, 1000.640],
                   "rag": ['#417505', '#f5a623', '#d0021b'],
                   "alert_size": [0.0, 2.1, 1000.6], }

        for column in results:
            for index in range(len(alert[column].values)):
                assert alert[column].values[index] == results[column][index]

        # testing with pd.series
        alert = utils.alarm_to_alert(self.sample_data_frame["float"], "float")

        results = {"alert": [0.001, 2.100, 1000.640],
                   "rag": ['#417505', '#f5a623', '#d0021b'],
                   "alert_size": [0.0, 2.1, 1000.6], }

        for column in results:
            for index in range(len(alert[column].values)):
                assert alert[column].values[index] == results[column][index]

        # testing with dict
        alert = utils.alarm_to_alert(self.sample_data_frame["float"].to_dict(),
                                     "float")

        results = {"alert": [0.001, 2.100, 1000.640],
                   "rag": ['#417505', '#f5a623', '#d0021b'],
                   "alert_size": [0.0, 2.1, 1000.6], }

        for column in results:
            for index in range(len(alert[column].values)):
                assert alert[column].values[index] == results[column][index]

    def test_create_random_subgraph(self):
        g = twin.get_graph("oxleas_wood_system.pkl", "examples")
        # test completely random
        g1 = utils.create_random_subgraph(g, 30)

        outcome = isinstance(g1, Graph)

        assert outcome
        assert len(g1.edges()) >= 30
        assert is_connected(g1)

        # test seeded run
        g1 = utils.create_random_subgraph(g, 30, 10)
        assert ('1103639|1105732|1107525', '1103639|1103647|1104458') in \
            g1.edges

        assert is_connected(g1)
