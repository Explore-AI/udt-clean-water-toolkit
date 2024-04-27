from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from cwa_geod.assets.models import DistributionMain
from cwa_geod.utilities.models import DMA


class Command(BaseCommand):
    help = "Write Thames Water distritribition mains layer data to sql"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="Path to gdb.zip")
        parser.add_argument("-x", "--index", type=int, help="Layer index")

    def handle(self, *args, **kwargs):
        zip_path = kwargs.get("file")
        layer_index = kwargs.get("index")

        ds = DataSource(zip_path)
        distribution_mains_layer = ds[layer_index]

        print(
            f"There are {distribution_mains_layer.num_feat} features. Large numbers of features will take a long time to save."
        )

        new_distribution_mains = []
        for feature in distribution_mains_layer:
            gid = feature.get("GISID")
            geom = feature.geom
            geom_4326 = feature.get("wkt_geom_4326")

            new_distribution_main = DistributionMain(
                gid=gid, geometry=geom.wkt, geometry_4326=geom_4326
            )
            new_distribution_mains.append(new_distribution_main)

            if len(new_distribution_mains) == 100000:
                DistributionMain.objects.bulk_create(new_distribution_mains)
                new_distribution_mains = []

        # save the last set of data as it will probably be less than 100000
        if new_distribution_mains:
            DistributionMain.objects.bulk_create(new_distribution_mains)

        DMAThroughModel = DistributionMain.dmas.through
        bulk_create_list = []
        for distribution_main in DistributionMain.objects.only("id", "geometry"):

            wkt = distribution_main.geometry.wkt

            dma_ids = DMA.objects.filter(geometry__intersects=wkt).values_list(
                "pk", flat=True
            )

            if not dma_ids:
                dma_ids = [DMA.objects.get(name=r"undefined").pk]

            for dma_id in dma_ids:
                bulk_create_list.append(
                    DMAThroughModel(
                        distributionmain_id=distribution_main.pk, dma_id=dma_id
                    )
                )

            if len(bulk_create_list) == 100000:
                DMAThroughModel.objects.bulk_create(bulk_create_list)
                bulk_create_list = []

        # save the last set of data as it will probably be less than 100000
        if bulk_create_list:
            DMAThroughModel.objects.bulk_create(bulk_create_list)
