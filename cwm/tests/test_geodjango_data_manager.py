import pytest

from cleanwater.data_managers import GeoDjangoDataManager
from cleanwater.exceptions import LayerLoadException


class TestGeoDjangoDataManager:

    def test_arg_invalid_zip_path(self):
        geodjango_data_manager = GeoDjangoDataManager()
        invalid_zip_path = "./invalid.zip"
        valid_layer_name = "a valid layer name"  # to replace with real valid layer name

        with pytest.raises(Exception) as exc_info:
            geodjango_data_manager.gdb_zip_to_gdf_layer(invalid_zip_path, valid_layer_name)
            assert exc_info.value.args[0] == "gdf file not found"

    def test_arg_invalid_layer_name(self):
        geodjango_data_manager = GeoDjangoDataManager()
        valid_zip_path = "a valid path"  # to replace with real valid path
        invalid_layer_name = "invalid_layer"

        with pytest.raises(LayerLoadException) as exc_info:
            geodjango_data_manager.gdb_zip_to_gdf_layer(valid_zip_path, invalid_layer_name)
            assert (
                exc_info.value.args[0]
                == f"Layer cannot be identified with provided name: {invalid_layer_name}"
            )
