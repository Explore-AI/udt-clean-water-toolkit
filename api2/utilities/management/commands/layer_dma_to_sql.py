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

    # def handle(self, *args, **kwargs):
    #     from django.contrib.gis.utils import LayerMapping
    #     zip_path = "/home/timol/work/exploreai/udt/data/CW_20231108_060001.gdb.zip"
    #     dma_mapping = {"code": "DMACODE", 'geometry': 'POINT'}

    #     ds = DataSource(zip_path)


    #     lm = LayerMapping(DMA, ds, dma_mapping, transform=False, layer=28)
    #     print(lm)

    def handle(self, *args, **kwargs):
        zip_path = kwargs.get("file")

        ds = DataSource(zip_path)

        for layer_values in LAYER_DATA.values():
            for layer_code in layer_values[1]:
                print(layer_code)
                self.add_data_from_layer(ds, layer_values[0], layer_code)

    def add_data_from_layer(self, ds, layer_index, layer_code):
        for feature in ds[layer_index]:
            layer_dma_code = feature.get(layer_code)

            if layer_dma_code:
                dma = DMA.objects.get_or_create(
                    code=layer_dma_code
                )
