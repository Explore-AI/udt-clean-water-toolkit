import os
import geopandas as gpd
from cleanwater.exceptions import LayerLoadException
from cleanwater.serializers import GeoDjangoSerializer
from .base_data_manager import BaseDataManager


class GeoDjangoDataManager(BaseDataManager, GeoDjangoSerializer):
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

    def django_queryset_to_geodataframe(self, qs, srid=None):
        # TODO: this class should probably not be instantiated here
        data = self.queryset_to_geojson(qs, srid)
        return gpd.read_file(data)
