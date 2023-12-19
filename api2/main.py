import sys, os
from django import setup

# https://stackoverflow.com/a/32590521
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
setup()

from app.geospatial.data_managers.twgs_data_manager import TWGS_DataManager


def gdf_to_sql():
    twdm = TWGS_DataManager()

    # layers = twdm.get_layer_list()

    #    gdf = twdm.wlogger_layer_gdb_to_gdf()
    # print(layers)

    # Have a look at the TWGS_DataManager
    # create additioal functions to convert csv to gdf
    # Create a django model for each layer
    # write to sql using the Model.objectscreate method here

    # run this file when in the api2 directory. ensure venv is activated


def create_dma_codes():
    pass
    # read in the layers from csv to gdf here
    # extract the dma code data
    # make a single list with a set of UNIQUE dma codes. each dma code should only appear once
    # Write this to the dma code table using the DMA.objects.create. You will need to import the DMA model.


def main():
    gdf_to_sql()


if __name__ == "__main__":
    main()
