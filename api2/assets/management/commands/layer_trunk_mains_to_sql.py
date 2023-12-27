from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from assets.models import TrunkMain
from utilities.models import DMA

TRUNK_MAINS_LAYER_INDEX = 9


class Command(BaseCommand):
    help = "Write Thames Water dma codes from geospatial layers of interest to sql"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="Path to gdb.zip")

    ### Attempt using bulk create
    def handle(self, *args, **kwargs):
        zip_path = kwargs.get("file")

        ds = DataSource(zip_path)
        trunk_main_layer = ds[TRUNK_MAINS_LAYER_INDEX]

        layer_gisids = trunk_main_layer.get_fields("GISID")
        layer_shapes_x = trunk_main_layer.get_fields("SHAPEX")
        layer_shapes_y = trunk_main_layer.get_fields("SHAPEY")
        layer_dma_codes = trunk_main_layer.get_fields("DMACODE")
        layer_geometries = trunk_main_layer.get_geoms()

        new_trunk_mains = []
        for (
            layer_gisid,
            layer_shape_x,
            layer_shape_y,
            layer_dma_code_1,
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
                "dma": layer_dma_code_1,
                "geometry": layer_geometry.wkt,
            }

            if not None in data.values():
                dma = DMA.objects.get(code=data["dma"])
                data["dma"] = dma
                new_trunk_mains.append(TrunkMain(**data))

        TrunkMain.objects.bulk_create(new_trunk_mains)
