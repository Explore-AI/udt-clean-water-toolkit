from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping
from cwa_geod.assets.models import NetworkOptValve
from cwa_geod.utilities.models import DMA


class Command(BaseCommand):
    help = "Write Thames Water network opt valve data to sql"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="Path to valid datasource")
        parser.add_argument("-x", "--index", type=int, help="Layer index")

    def handle(self, *args, **kwargs):
        ds_path = kwargs.get("file")
        layer_index = kwargs.get("index")

        ds = DataSource(ds_path)

        print(
            f"""There are {ds[layer_index].num_feat} features.
Large numbers of features will take a long time to save."""
        )

        layer_mapping = {
            "gid": "GISID",
            "acoustic_logger" : "Acoustic_Logger",
            "geometry": "POINT",
        }

        lm = LayerMapping(
            NetworkOptValve, ds, layer_mapping, layer=layer_index, transform=False
        )
        lm.save(strict=True)
        DMAThroughModel = NetworkOptValve.dmas.through
        bulk_create_list = []
        for network_opt_valve in NetworkOptValve.objects.only("id", "geometry"):
            wkt = network_opt_valve.geometry.wkt

            dma_ids = DMA.objects.filter(geometry__intersects=wkt).values_list(
                "pk", flat=True
            )

            if not dma_ids:
                dma_ids = [DMA.objects.get(name=r"undefined").pk]
            bulk_create_list.extend(
                [
                    DMAThroughModel(
                        networkoptvalve_id=network_opt_valve.pk, dma_id=dma_id
                    )
                    for dma_id in dma_ids
                ]
            )
            # network_opt_valve.dmas.add(*list(dma_ids))

        DMAThroughModel.objects.bulk_create(bulk_create_list, batch_size=375000)
