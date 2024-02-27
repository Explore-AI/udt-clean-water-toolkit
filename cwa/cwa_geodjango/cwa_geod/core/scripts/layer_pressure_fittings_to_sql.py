from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from cwa_geod.assets.models import PressureFitting
from cwa_geod.utilities.models import DMA

PRESSURE_FITTING_LAYER_INDEX = 19
DMA_FIELD_NAME = "DMACODE"


class Command(BaseCommand):
    help = "Write Thames Water pressure fitting layer data to sql"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="Path to vector data source")
        parser.add_argument("-x", "--layer_index", type=str, help="Layer index")

    ### Attempt using bulk create
    def handle(self, *args, **kwargs):
        zip_path = kwargs.get("file")
        layer_index = kwargs.get("layer_index")

        ds = DataSource(zip_path)
        pressure_fitting_layer = ds[layer_index]

        layer_gisids = pressure_fitting_layer.get_fields("GISID")
        layer_geometries = pressure_fitting_layer.get_geoms()

        print(
            f"There are {pressure_fitting_layer.num_feat} features. Large numbers of features will take a long time to save."
        )

        new_pressure_fittings = []
        for (
            layer_gisid,
            layer_geometry,
        ) in zip(
            layer_gisids,
            layer_geometries,
        ):
            data = {
                "gisid": layer_gisid,
                "geometry": layer_geometry.wkt,
            }

            if not None in data.values():
                dma = DMA.objects.get(code=data["dma"])
                data["dma"] = dma
                new_pressure_fittings.append(PressureFitting(**data))

        PressureFitting.objects.bulk_create(new_pressure_fittings)
