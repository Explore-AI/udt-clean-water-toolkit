from cleanwater.data_managers import GeospatialDataManager


class TWGS_DataManager(GeospatialDataManager):
    def tw_wlogger_layer_to_sql():
        """Retrieve the TW clean water wlogger layer
        and save the rows to sql.
        """
        self.gdm.gdb_zip_to_gdf_layer(zip_file_path, "wLogger")
