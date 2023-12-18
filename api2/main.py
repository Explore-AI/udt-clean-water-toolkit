import sys, os
from django import setup

# https://stackoverflow.com/a/32590521
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
setup()

from app.geospatial.data_managers.twgs_data_manager import TWGS_DataManager


def gdf_to_sql():
    twdm = TWGS_DataManager()

    layers = twdm.get_layer_list()

    gdf = twdm.wlogger_layer_gdb_to_gdf()

    # Have a look at the TWGS_DataManager
    # create additioal functions to convert csv to gdf
    # Create a django model for each layer
    # write to sql using the Model.create method here

    # run this file when in the api2 directory. ensure venv is activated


def main():
    gdf_to_sql()


if __name__ == "__main__":
    main()
