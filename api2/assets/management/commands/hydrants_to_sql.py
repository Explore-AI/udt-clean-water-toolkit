from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from assets.models import Hydrant

LAYER_DATA = {"wHydrant": 28}


class Command(BaseCommand):
    help = "Write Thames Water dma codes from geospatial layers of interest to sql"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="Path to gdb.zip")

    def handle(self, *args, **kwargs):
        from django.contrib.gis.utils import LayerMapping

        zip_path = "/home/timol/work/exploreai/udt/data/CW_20231108_060001.gdb.zip"
        hydrant_mapping = {
            "dma": {"code": "DMACODE"},
            "gisid": "GISID",
            "shape_x": "SHAPEX",
            "shape_y": "SHAPEY",
            "geometry": "POINT",
        }

        ds = DataSource(zip_path)

        # https://stackoverflow.com/questions/50597101/django-core-exceptions-fielddoesnotexist-buildingaddress-has-no-field-named-fa

        # https://stackoverflow.com/questions/21197483/geodjango-layermapping-foreign-key
        lm = LayerMapping(Hydrant, ds, hydrant_mapping, transform=False, layer=28)
        lm.save(strict=True, verbose=True, progress=True)
