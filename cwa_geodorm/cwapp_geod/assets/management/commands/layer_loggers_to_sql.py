from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from ..assets.models import Logger
from ...utilities.models import DMA

LOGGER_LAYER_INDEX = 2
DMA_FIELD_NAME = "DMACODE1"

import pdb

pdb.set_trace()


class Command(BaseCommand):
    help = "Write Thames Water logger layer data to sql"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="Path to gdb.zip")

    ### Attempt using bulk create
    def handle(self, *args, **kwargs):
        zip_path = kwargs.get("file")

        ds = DataSource(zip_path)
        logger_layer = ds[LOGGER_LAYER_INDEX]

        print(
            f"There are {logger_layer.num_feat} features. Large numbers of features will take a long time to save."
        )

        layer_gisids = logger_layer.get_fields("GISID")
        layer_shapes_x = logger_layer.get_fields("SHAPEX")
        layer_shapes_y = logger_layer.get_fields("SHAPEY")
        layer_dma_codes_1 = logger_layer.get_fields(DMA_FIELD_NAME)
        layer_geometries = logger_layer.get_geoms()

        new_loggers = []
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
            layer_dma_codes_1,
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
                new_loggers.append(Logger(**data))

        Logger.objects.bulk_create(new_loggers)

    ### This can be done more efficiently with the bulk create method
    # def handle(self, *args, **kwargs):
    #     zip_path = kwargs.get("file")

    #     ds = DataSource(zip_path)
    #     logger_layer_index = 2
    #     logger_layer = ds[logger_layer_index]

    #     for feature in logger_layer:
    #         data = [
    #             feature.get("GISID"),
    #             feature.get("SHAPEX"),
    #             feature.get("SHAPEY"),
    #             feature.geom.wkt,
    #             feature.get("DMACODE1"),
    #         ]

    #         if not None in data:
    #             dma = DMA.objects.filter(code=data[4]).first()

    #             Logger.objects.get_or_create(
    #                 gisid=data[0],
    #                 shape_x=data[1],
    #                 shape_y=data[2],
    #                 geometry=data[3],
    #                 dma=dma,
    #             )
