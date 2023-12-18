from cleanwater.data_managers import GeospatialDataManager
from ...config.settings import TW_GS_CLEAN_WATER_ZIP_PATH


class TWGS_DataManager(GeospatialDataManager):
    def wlogger_layer_to_sql(self):
        """Retrieve the TW clean water wlogger layer
        and save the rows to sql.
        """
        return self.gdb_zip_to_gdf_layer(TW_GS_CLEAN_WATER_ZIP_PATH, "wLogger")
