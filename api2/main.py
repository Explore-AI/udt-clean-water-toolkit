import sys, os
from django import setup

# https://stackoverflow.com/a/32590521
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
setup()
#from app.geospatial.data_managers.twgs_data_manager import TWGS_DataManager
from django.contrib.gis.gdal import DataSource
from utilities.models import DMA
from assets.models import distribution_main, hydrant, logger, network_meter, trunk_main



#def gdf_to_sql():
#    twdm = TWGS_DataManager()

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
    ds = DataSource("/Users/annegret/Documents/Enterprise/practicedata/CW_20231108_060001.gdb.zip")

    # NetworkMeter DMA1CODE
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


    # NetworkMeter DMA2CODE
    for feature in ds[26]:
        layer_dma_code = feature.get("DMA2CODE")

        if layer_dma_code:
            does_dma_code_already_exist = DMA.objects.filter(
                code=layer_dma_code
            ).exists()

            if does_dma_code_already_exist:
                continue

            dma = DMA.objects.create(code=layer_dma_code)
            dma.save()


    # TrunkMain DMACODE
    for feature in ds[9]:
        layer_dma_code = feature.get("DMACODE")

        if layer_dma_code:
            does_dma_code_already_exist = DMA.objects.filter(
                code=layer_dma_code
            ).exists()

            if does_dma_code_already_exist:
                continue

            dma = DMA.objects.create(code=layer_dma_code)
            dma.save()

    # DistributionMain DMACODE
    for feature in ds[10]:
        layer_dma_code = feature.get("DMACODE")

        if layer_dma_code:
            does_dma_code_already_exist = DMA.objects.filter(
                code=layer_dma_code
            ).exists()

            if does_dma_code_already_exist:
                continue

            dma = DMA.objects.create(code=layer_dma_code)
            dma.save()

    # Hydrant DMACODE
    for feature in ds[28]:
        layer_dma_code = feature.get("DMACODE")

        if layer_dma_code:
            does_dma_code_already_exist = DMA.objects.filter(
                code=layer_dma_code
            ).exists()

            if does_dma_code_already_exist:
                continue

            dma = DMA.objects.create(code=layer_dma_code)
            dma.save()

    # Logger DMACODE1
    for feature in ds[2]:
        layer_dma_code = feature.get("DMACODE1")

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
