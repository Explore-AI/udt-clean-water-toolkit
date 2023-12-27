from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.gdal.error import GDALException
from assets.models import DistributionMain
from utilities.models import DMA

DISTRIBUTION_MAINS_LAYER_INDEX = 10


class Command(BaseCommand):
    help = "Write Thames Water dma codes from geospatial layers of interest to sql"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="Path to gdb.zip")

    def handle(self, *args, **kwargs):
        zip_path = kwargs.get("file")

        ds = DataSource(zip_path)
        distribution_main_layer = ds[DISTRIBUTION_MAINS_LAYER_INDEX]

        new_distribution_mains = []

        for feature in distribution_main_layer:
            gisid = feature.get("GISID")
            dma_code = feature.get("DMACODE")
            shape_length = feature.get("SHAPE_Length")

            # Had to to the except as got this error
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

        DistributionMain.objects.bulk_create(new_distribution_mains)
