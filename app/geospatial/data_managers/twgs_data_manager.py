import fiona
from cleanwater.data_managers import GeospatialDataManager
from ...config.settings import TW_GS_CLEAN_WATER_ZIP_PATH


class TWGS_DataManager(GeospatialDataManager):
    def get_layer_list(self):
        """Retrieve the TW clean water layer list"""
        return fiona.listlayers(TW_GS_CLEAN_WATER_ZIP_PATH)

    def wlogger_layer_gdb_to_gdf(self):
        """Retrieve the TW clean water wlogger layer as a geodataframe."""
        return self.gdb_zip_to_gdf_layer(TW_GS_CLEAN_WATER_ZIP_PATH, "wLogger")

    def wlogger_layer_csv_to_gdf(self):
        """Retrieve the TW clean water wlogger layer csv as a geodataframe."""
        pass
