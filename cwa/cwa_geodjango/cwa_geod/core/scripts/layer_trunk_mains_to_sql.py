from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.gdal.error import GDALException
from cwa_geod.assets.models import TrunkMain
from cwa_geod.utilities.models import DMA

TRUNK_MAINS_LAYER_INDEX = 4
DMA_FIELD_NAME = "DMACODE"


class Command(BaseCommand):
    help = "Write Thames Water trunk mains layer data to sql"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="Path to gdb.zip")
        parser.add_argument("-x", "--index", type=str, help="Layer index")

    ### This method doesn't work because of errors in the geometry object
    def handle(self, *args, **kwargs):
        zip_path = kwargs.get("file")
        layer_index = kwargs.get("layer_index")

        ds = DataSource(zip_path)
        trunk_main_layer = ds[4]

        layer_gis_ids = trunk_main_layer.get_fields("GISID")
        layer_geometries = trunk_main_layer.get_geoms()

        new_trunk_mains = []
        for gid, geometry in zip(layer_gis_ids, layer_geometries):
            dmas = DMA.objects.filter(geometry_multipolygon__intersects=geometry)

            new_trunk_main = TrunkMain(gid=gid, geometry=geometry, dma=dmas)
            new_trunk_mains.append(new_trunk_main)

            if len(new_trunk_mains) == 100000:
                TrunkMain.objects.bulk_create(new_trunk_mains)
                new_trunk_mains = []

        # save the last set of data as it will probably be less than 100000
        if new_trunk_mains:
            TrunkMain.objects.bulk_create(new_trunk_mains)
