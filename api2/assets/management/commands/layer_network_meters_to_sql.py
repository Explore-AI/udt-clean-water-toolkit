from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from assets.models import NetworkMeter
from utilities.models import DMA

NETWORK_METERS_LAYER_INDEX = 9


class Command(BaseCommand):
    help = "Write Thames Water dma codes from geospatial layers of interest to sql"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="Path to gdb.zip")

    ### Attempt using bulk create
    def handle(self, *args, **kwargs):
        zip_path = kwargs.get("file")

        ds = DataSource(zip_path)
        network_meter_layer = ds[NETWORK_METERS_LAYER_INDEX]

        layer_gisids = network_meter_layer.get_fields("GISID")
        layer_shapes_x = network_meter_layer.get_fields("SHAPEX")
        layer_shapes_y = network_meter_layer.get_fields("SHAPEY")
        layer_dma_codes_1 = network_meter_layer.get_fields("DMA1CODE")
        layer_dma_codes_2 = network_meter_layer.get_fields("DMA2CODE")
        layer_geometries = network_meter_layer.get_geoms()

        new_network_meters = []
        for (
            layer_gisid,
            layer_shape_x,
            layer_shape_y,
            layer_dma_code_1,
            layer_dma_code_2,
            layer_geometry,
        ) in zip(
            layer_gisids,
            layer_shapes_x,
            layer_shapes_y,
            layer_dma_codes_1,
            layer_dma_codes_2,
            layer_geometries,
        ):
            data = {
                "gisid": layer_gisid,
                "shape_x": layer_shape_x,
                "shape_y": layer_shape_y,
                "dma_1": layer_dma_code_1,
                "dma_2": layer_dma_code_2,
                "geometry": layer_geometry.wkt,
            }

            if not None in data.values():
                dma_1 = DMA.objects.get(code=data["dma_1"])
                dma_2 = DMA.objects.get(code=data["dma_2"])
                data["dma_1"] = dma_1
                data["dma_2"] = dma_2

                new_network_meters.append(NetworkMeter(**data))

        NetworkMeter.objects.bulk_create(new_network_meters)
