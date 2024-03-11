import csv
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry
from cwa_geod.utilities.models import DMA, Utility
from cwa_geod.core.constants import DEFAULT_SRID


class Command(BaseCommand):
    help = "Write Thames Water dma codes from geospatial layers of interest to sql"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="Path to dma csv")

    ### Attempt using bulk create
    def handle(self, *args, **kwargs):
        dma_file = kwargs.get("file")

        dma_name_idx = 1
        dma_code_idx = 2
        geom_column_idx = 3

        utility, _ = Utility.objects.get_or_create(name="THAMES WATER")

        # Create a dummy dma as not all assets fall within a dma
        DMA.objects.create(
            utility=utility,
            name=r"undefined",
            code=r"undefined",
            geometry=GEOSGeometry("MULTIPOLYGON EMPTY", srid=DEFAULT_SRID),
        )

        new_dmas = []
        with open(dma_file) as infile:
            csv_reader = csv.reader(infile, delimiter=",")
            next(csv_reader)

            for row in csv_reader:
                dma_geom = GEOSGeometry(row[geom_column_idx], srid=DEFAULT_SRID)

                new_dma = DMA(
                    utility=utility,
                    name=row[dma_name_idx],
                    code=row[dma_code_idx],
                    geometry=dma_geom,
                )

                new_dmas.append(new_dma)
                if len(new_dmas) == 100000:
                    DMA.objects.bulk_create(new_dmas)
                    new_dmas = []

        # save the last set of data as it will probably be less than 100000
        if new_dmas:
            DMA.objects.bulk_create(new_dmas)
