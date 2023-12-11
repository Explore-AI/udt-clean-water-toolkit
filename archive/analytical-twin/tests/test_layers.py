import data_factory.AnalyticalTwin.layers as layers
import datetime
from tempfile import mkdtemp
from pathlib import Path
import json
import shutil


class TestLayersModule:
    @classmethod
    def setup_class(cls):
        cls.temp_path = Path(mkdtemp())
        print(cls.temp_path)

    @classmethod
    def teardown_class(cls):
        shutil.rmtree(cls.temp_path)

    def test_validate_dict(self):
        # correct format
        layer_dict = {"node": {"1718223": {"start_date": "2018-05-03 11:54:00",
                                           "end_date": "2021-04-08 03:30:00"}},
                      "edge": {"1112210": {"test_attribute": 2000}},
                      "edge_key": "GISID"
                      }
        assert layers.validate_dict(layer_dict)

        # wrong keys
        layer_dict = {"node": {"1718223": {"start_date": "2018-05-03 11:54:00",
                                           "end_date": "2021-04-08 03:30:00"}},
                      "edge": {"1112210": {"test_attribute": 2000}}
                      }
        try:
            layers.validate_dict(layer_dict)
        except Exception as E:
            assert str(E) == 'The dictionary is missing the following' \
                             ' key(s) {\'edge_key\'}'

        # wrong type of value of edge_key
        layer_dict = {"node": {"1718223": {"start_date": "2018-05-03 11:54:00",
                                           "end_date": "2021-04-08 03:30:00"}},
                      "edge": {"1112210": {"test_attribute": 2000}},
                      "edge_key": {"GISID"}
                      }
        try:
            layers.validate_dict(layer_dict)
        except Exception as E:
            assert str(E) == 'Value of the \'edge_key\' key should be' \
                             ' string, not <class \'dict\'>'

    def test_export_json(self):
        layer_dict = {"node": {"1718223": {"start_date": datetime.datetime(
            2017, 8, 10, 15, 0),
            "end_date": datetime.datetime(2017, 9, 1, 2, 0)}},
            "edge": {"1112210": {"test_attribute": 2000}},
            "edge_key": "GISID"
        }

        layers.export_json(layer_dict, 'test',
                           datetime.datetime(2017, 9, 1, 2, 0),
                           path=self.temp_path)

        test_file = self.temp_path / 'Layers' / \
            'test' / 'test_20170901_020000.json'
        assert test_file.exists()

        with open(test_file, 'r') as dumped_dict:
            loaded_dict = json.load(dumped_dict)

        assert loaded_dict["node"]["1718223"]["start_date"] \
               == '2017-08-10 15:00:00'
