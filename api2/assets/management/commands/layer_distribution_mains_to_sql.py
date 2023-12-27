from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.gdal.error import GDALException
from assets.models import DistributionMain
from utilities.models import DMA

DISTRIBUTION_MAINS_LAYER_INDEX = 10


class Command(BaseCommand):
    help = "Write Thames Water distritribition mains layer data to sql"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="Path to gdb.zip")

    def handle(self, *args, **kwargs):
        zip_path = kwargs.get("file")

        ds = DataSource(zip_path)
        distribution_mains_layer = ds[DISTRIBUTION_MAINS_LAYER_INDEX]

        print(
            f"There are {distribution_mains_layer.num_feat} features. Large numbers of features will take a long time to save."
        )

        new_distribution_mains = []
        for feature in distribution_mains_layer:
            gisid = feature.get("GISID")
            dma_code = feature.get("DMACODE")
            shape_length = feature.get("SHAPE_Length")

            # Had to to the except as got this error:
            # django.contrib.gis.gdal.error.GDALException: Invalid OGR Integer Type: 11
            try:
                geometry = feature.geom
            except GDALException:
                continue

            data = {
                "gisid": gisid,
                "dma": dma_code,
                "shape_length": shape_length,
                "geometry": geometry.wkt,
            }

            if not None in data.values():
                dma = DMA.objects.get(code=data["dma"])
                data["dma"] = dma
                new_distribution_mains.append(DistributionMain(**data))

            if len(new_distribution_mains) == 100000:
                DistributionMain.objects.bulk_create(new_distribution_mains)
                new_distribution_mains = []
