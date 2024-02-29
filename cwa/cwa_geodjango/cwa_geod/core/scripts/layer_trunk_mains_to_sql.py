from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from cwa_geod.assets.models import TrunkMain
from cwa_geod.utilities.models import DMA


TRUNK_MAINS_LAYER_INDEX = 4
DMA_FIELD_NAME = "DMACODE"


class Command(BaseCommand):
    help = "Write Thames Water trunk mains layer data to sql"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="Path to gdb.zip")
        parser.add_argument("-x", "--index", type=int, help="Layer index")

    def handle(self, *args, **kwargs):
        import pdb
        pdb.set_trace()

        zip_path = kwargs.get("file")
        layer_index = kwargs.get("index")

        ds = DataSource(zip_path)

        trunk_main_layer = ds[layer_index]

        layer_gis_ids = trunk_main_layer.get_fields("GISID")
        layer_geometries = trunk_main_layer.get_geoms()

        new_trunk_mains = []
        for gid, geom in zip(layer_gis_ids, layer_geometries):
            dma_wkt = "%s" % geom.wkt
            dma_intersection = DMA.objects.filter(geometry__intersects=dma_wkt)

            if not dma_intersection:
                dma_intersection = 'NA'

            new_trunk_main = TrunkMain(gid=gid, geometry=geom.wkt)
            new_trunk_main.save()

            if dma_intersection and dma_intersection != 'NA':
                new_trunk_main.dma.add(dma_intersection)
                print(new_trunk_main.dma)

            new_trunk_mains.append(new_trunk_main)

            if len(new_trunk_mains) == 100000:
                TrunkMain.objects.bulk_create(new_trunk_mains)
                new_trunk_mains = []

        if new_trunk_mains:
            TrunkMain.objects.bulk_create(new_trunk_mains)
