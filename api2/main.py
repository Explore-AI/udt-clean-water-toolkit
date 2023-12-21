import sys, os
from django import setup

# https://stackoverflow.com/a/32590521
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
setup()
from app.geospatial.data_managers.twgs_data_manager import TWGS_DataManager
from django.contrib.gis.gdal import DataSource
from utilities.models import DMA


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

    # layer_indices = {
    #     "wNetworkMeter": 26,
    #     "wTrunkMains": 9,
    #     "wDistributionMain": 10,
    #     "wHydrant": 28,
    #     "wLogger": 2,
    # }


def create_dma_codes():
    ds = DataSource("/home/timol/work/exploreai/udt/data/CW_20231108_060001.gdb.zip")

    for feature in ds[26]:
        layer_dma_code = feature.get("DMA1CODE")

        if layer_dma_code:
            does_dma_code_already_exist = DMA.objects.filter(
                code=layer_dma_code
            ).exists()

            if does_dma_code_already_exist:
                continue

            dma = DMA.objects.create(code=layer_dma_code)
            dma.save()


def main():
    create_dma_codes()


if __name__ == "__main__":
    main()
