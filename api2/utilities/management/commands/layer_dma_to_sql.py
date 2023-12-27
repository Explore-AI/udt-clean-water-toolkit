from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from utilities.models import DMA

LAYER_DATA = {
    "wHydrant": [28, ["DMACODE"]],
    "wLogger": [2, ["DMACODE1"]],
    "wNetworkMeter": [26, ["DMA1CODE", "DMA2CODE"]],
    "wTrunkMains": [9, ["DMACODE"]],
    #    "wDistributionMain": [10, ["DMACODE"]],
}


class Command(BaseCommand):
    help = "Write Thames Water dma codes from geospatial layers of interest to sql"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="Path to gdb.zip")

    ### The below two functions use the get_or_create approach but is slow.
    def handle(self, *args, **kwargs):
        zip_path = kwargs.get("file")

        ds = DataSource(zip_path)

        for layer_name, layer_values in LAYER_DATA.items():
            print(f"Reading in data from layer: {layer_name}")
            for layer_code in layer_values[1]:
                self.add_data_from_layer(ds, layer_values[0], layer_code)

    def add_data_from_layer(self, ds, layer_index, layer_code):
        for feature in ds[layer_index]:
            layer_dma_code = feature.get(layer_code)

            if layer_dma_code:
                dma = DMA.objects.get_or_create(code=layer_dma_code)


### Attempt using bulk create
# def handle(self, *args, **kwargs):
#     zip_path = kwargs.get("file")

#     ds = DataSource(zip_path)

#     for layer_name, layer_values in LAYER_DATA.items():
#         print(f"Reading in data from layer: {layer_name}")
#         for layer_code in layer_values[1]:
#             self.add_data_from_layer(ds, layer_values[0], layer_code)

# def add_data_from_layer(self, ds, layer_index, layer_code):
#     def _get_feature_data(feature):
#         feature.get(layer_code)

#     all_dma_codes_from_layer = list(map(_get_feature_data, ds[layer_index]))
#     import pdb

#     pdb.set_trace()

#     # all_dma_codes_from_layer = [
#     #     feature.get(layer_code) for feature in ds[layer_index]
#     # ]

#     dmas_that_already_exist_in_sql = DMA.objects.filter(
#         code__in=all_dma_codes_from_layer
#     ).values_list("code", flat=True)

#     dmas_not_in_sql = set(all_dma_codes_from_layer) - set(
#         dmas_that_already_exist_in_sql
#     )


### This below function should allow for dma layermapping directly
# def handle(self, *args, **kwargs):
#     from django.contrib.gis.utils import LayerMapping
#     zip_path = "/home/timol/work/exploreai/udt/data/CW_20231108_060001.gdb.zip"
#     dma_mapping = {"code": "DMACODE", 'geometry': 'POINT'}

#     ds = DataSource(zip_path)


#     lm = LayerMapping(DMA, ds, dma_mapping, transform=False, layer=28)
#     print(lm)
