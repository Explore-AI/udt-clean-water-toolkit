from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from assets.models import Hydrant
from utilities.models import DMA

LAYER_DATA = {"wHydrant": 28}


class Command(BaseCommand):
    help = "Write Thames Water dma codes from geospatial layers of interest to sql"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="Path to gdb.zip")

    # def handle(self, *args, **kwargs):
    #     from django.contrib.gis.utils import LayerMapping

    #     zip_path = kwargs.get("file")
    #     hydrant_mapping = {
    #         "dma": {"code": "DMACODE"},
    #         "gisid": "GISID",
    #         "shape_x": "SHAPEX",
    #         "shape_y": "SHAPEY",
    #         "geometry": "POINT",
    #     }

    #     ds = DataSource(zip_path)

    #     # https://stackoverflow.com/questions/50597101/django-core-exceptions-fielddoesnotexist-buildingaddress-has-no-field-named-fa

    #     # https://stackoverflow.com/questions/21197483/geodjango-layermapping-foreign-key
    #     lm = LayerMapping(Hydrant, ds, hydrant_mapping, transform=False, layer=28)
    #     lm.save(strict=True, verbose=True, progress=True)

    def handle(self, *args, **kwargs):
        zip_path = kwargs.get("file")

        ds = DataSource(zip_path)
        hydrant_layer_index = 28
        hydrant_layer = ds[hydrant_layer_index]

        for feature in hydrant_layer:
            data = [
                feature.get("GISID"),
                feature.get("SHAPEX"),
                feature.get("SHAPEY"),
                feature.geom.wkt,
                feature.get("DMACODE"),
            ]

            if not None in data:
                dma = DMA.objects.filter(code=data[4]).first()

                Hydrant.objects.create(
                    gisid=data[0],
                    shape_x=data[1],
                    shape_y=data[2],
                    geometry=data[3],
                    dma=dma,
                )
