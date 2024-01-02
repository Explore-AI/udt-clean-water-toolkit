import os
import geopandas as gpd
from .base_data_manager import BaseDataManager
from cleanwater.exceptions import LayerLoadException


class GeospatialDataManager(BaseDataManager):
    """Helper functions to manipulate geospatial data"""

    def gdb_zip_to_gdf_layer(self, zip_path: str, layer_name: str):
        if not os.path.exists(zip_path):
            raise Exception("gdf file not found")

        try:
            return gpd.read_file(zip_path, layer=layer_name)
        except ValueError:
            raise LayerLoadException(
                f"Layer cannot be identified with provided name: {layer_name}"
            )
