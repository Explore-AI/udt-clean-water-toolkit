from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.gdal.error import GDALException
from cwa_geod.assets.models import TrunkMain
from cwa_geod.utilities.models import DMA

TRUNK_MAINS_LAYER_INDEX = 9
DMA_FIELD_NAME = "DMACODE"


class Command(BaseCommand):
    help = "Write Thames Water trunk mains layer data to sql"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="Path to gdb.zip")

    ### This method doesn't work because of errors in the geometry object
    # def handle(self, *args, **kwargs):
    #     zip_path = kwargs.get("file")

    #     ds = DataSource(zip_path)
    #     trunk_main_layer = ds[TRUNK_MAINS_LAYER_INDEX]

    #     layer_gisids = trunk_main_layer.get_fields("GISID")
    #     layer_dma_codes = trunk_main_layer.get_fields("DMACODE")
    #     layer_geometries = trunk_main_layer.get_geoms()

    #     new_trunk_mains = []
    #     for (
    #         layer_gisid,
    #         layer_dma_code_1,
    #         layer_geometry,
    #     ) in zip(
    #         layer_gisids,
    #         layer_dma_codes,
    #         layer_geometries,
    #     ):
    #         data = {
    #             "gisid": layer_gisid,
    #             "dma": layer_dma_code_1,
    #             "geometry": layer_geometry.wkt,
    #         }

    #         if not None in data.values():
    #             dma = DMA.objects.get(code=data["dma"])
    #             data["dma"] = dma
    #             new_trunk_mains.append(TrunkMain(**data))

    #     TrunkMain.objects.bulk_create(new_trunk_mains)

    def handle(self, *args, **kwargs):
        zip_path = kwargs.get("file")

        ds = DataSource(zip_path)
        trunk_mains_layer = ds[TRUNK_MAINS_LAYER_INDEX]

        print(
            f"There are {trunk_mains_layer.num_feat} features. Large numbers of features will take a long time to save."
        )

        new_trunk_mains = []
        for feature in trunk_mains_layer:
            gisid = feature.get("GISID")
            dma_code = feature.get(DMA_FIELD_NAME)
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
                new_trunk_mains.append(TrunkMain(**data))

        TrunkMain.objects.bulk_create(new_trunk_mains)
