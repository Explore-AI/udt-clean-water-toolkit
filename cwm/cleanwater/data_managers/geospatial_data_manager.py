import sys, os
import geopandas as gpd
import fiona
from .base_data_manager import BaseDataManager
from exceptions import LayerLoadException


class GeospatialDataManager(BaseDataManager):
    def gdb_zip_to_gdf_layer(self, zip_path: str, layer_name: str):
        if not os.path.exists(zip_path):
            raise

        try:
            gdf = gpd.read_file(zip_path, layer=layer_name)
        except ValueError:
            LayerLoadException(
                f"Layer cannot be identified with provided name: {layer_name}"
            )
        print("yellow")
        return gdf
