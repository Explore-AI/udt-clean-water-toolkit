from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping
from cwa_geod.assets.models import TrunkMain
from cwa_geod.utilities.models import DMA


class Command(BaseCommand):
    help = "Write Thames Water trunk mains layer data to sql"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="Path to valid datasource")
        parser.add_argument("-x", "--index", type=int, help="Layer index")

    def handle(self, *args, **kwargs):
        zip_path = kwargs.get("file")
        layer_index = kwargs.get("index")

        ds = DataSource(zip_path)

        print(
            f"""There are {ds[layer_index].num_feat} features.
Large numbers of features will take a long time to save."""
        )

        layer_mapping = {
            "gid": "GISID",
            "geometry": "MULTILINESTRING",
        }

        lm = LayerMapping(
            TrunkMain, ds, layer_mapping, layer=layer_index, transform=False
        )
        lm.save(strict=True)

        for trunk_main in TrunkMain.objects.only("id", "geometry"):
            wkt = trunk_main.geometry.wkt

            dma_ids = DMA.objects.filter(geometry__intersects=wkt).values_list(
                "pk", flat=True
            )

            if not dma_ids:
                dma_ids = [DMA.objects.get(name=r"undefined").pk]

            trunk_main.dmas.add(*list(dma_ids))
