from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from cwa_geod.assets.models import Hydrant
from cwa_geod.utilities.models import DMA

HYDRANT_LAYER_INDEX = 28
DMA_FIELD_NAME = "DMACODE"


class Command(BaseCommand):
    help = "Write Thames Water hydrant layer data to sql"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="Path to gdb.zip")

    ### Attempt using bulk create
    def handle(self, *args, **kwargs):
        zip_path = kwargs.get("file")

        ds = DataSource(zip_path)
        hydrant_layer = ds[HYDRANT_LAYER_INDEX]

        print(
            f"There are {hydrant_layer.num_feat} features. Large numbers of features will take a long time to save."
        )

        layer_gisids = hydrant_layer.get_fields("GISID")
        layer_shapes_x = hydrant_layer.get_fields("SHAPEX")
        layer_shapes_y = hydrant_layer.get_fields("SHAPEY")
        layer_dma_codes = hydrant_layer.get_fields(DMA_FIELD_NAME)
        layer_geometries = hydrant_layer.get_geoms()

        new_hydrants = []
        for (
            layer_gisid,
            layer_shape_x,
            layer_shape_y,
            layer_dma_code,
            layer_geometry,
        ) in zip(
            layer_gisids,
            layer_shapes_x,
            layer_shapes_y,
            layer_dma_codes,
            layer_geometries,
        ):
            data = {
                "gisid": layer_gisid,
                "shape_x": layer_shape_x,
                "shape_y": layer_shape_y,
                "dma": layer_dma_code,
                "geometry": layer_geometry.wkt,
            }

            if not None in data.values():
                dma = DMA.objects.get(code=data["dma"])
                data["dma"] = dma
                new_hydrants.append(Hydrant(**data))

        Hydrant.objects.bulk_create(new_hydrants)
