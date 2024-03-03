from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping
from cwa_geod.assets.models import DistributionMain
from cwa_geod.utilities.models import DMA
from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = "Write Thames Water distribution mains layer data to sql"

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
            "geometry": "MULTILINESTRING",
        }

        lm = LayerMapping(
            DistributionMain, ds, layer_mapping, layer=layer_index, transform=False
        )
        lyr = ds[layer_index]
        for feat in lyr:
            gid = feat.get("GISID")
            if DistributionMain.objects.filter(gid=gid).exists():
                continue

            try:
                lm.save(strict=True, fid_range=(feat.fid, feat.fid + 1), step=1000000)
            except IntegrityError as err:
                if "identifier" in str(err):
                    raise ValidationError({"identifier": "This identifier is already in use."}) from err
                raise err

        for distribution_main in DistributionMain.objects.only("id", "geometry"):
            wkt = distribution_main.geometry.wkt

            dma_ids = DMA.objects.filter(geometry__intersects=wkt).values_list(
                "pk", flat=True
            )

            if not dma_ids:
                dma_ids = [DMA.objects.get(name=r"undefined").pk]

            distribution_main.dmas.add(*list(dma_ids))
