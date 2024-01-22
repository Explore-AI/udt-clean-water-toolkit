from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from cwa_geod.assets.models import PressureControlValve
from cwa_geod.utilities.models import DMA

PRESSURE_CONT_VALVE_LAYER_INDEX = 22
DMA_FIELD_NAME_1 = "DMA1CODE"
DMA_FIELD_NAME_2 = "DMA2CODE"


class Command(BaseCommand):
    help = "Write Thames Water pressure control valve layer data to sql"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="Path to gdb.zip")

    ### Attempt using bulk create
    def handle(self, *args, **kwargs):
        zip_path = kwargs.get("file")

        ds = DataSource(zip_path)
        import pdb

        pdb.set_trace()
        pressure_control_valve_layer = ds[PRESSURE_CONT_VALVE_LAYER_INDEX]

        print(
            f"There are {pressure_control_valve_layer.num_feat} features. Large numbers of features will take a long time to save."
        )

        layer_gisids = pressure_control_valve_layer.get_fields("GISID")
        layer_shapes_x = pressure_control_valve_layer.get_fields("SHAPEX")
        layer_shapes_y = pressure_control_valve_layer.get_fields("SHAPEY")
        layer_dma_codes_1 = pressure_control_valve_layer.get_fields(DMA_FIELD_NAME_1)
        layer_dma_codes_2 = pressure_control_valve_layer.get_fields(DMA_FIELD_NAME_2)
        layer_geometries = pressure_control_valve_layer.get_geoms()

        new_pressure_control_valves = []
        zipped_layer_data = zip(
            layer_gisids,
            layer_shapes_x,
            layer_shapes_y,
            layer_dma_codes_1,
            layer_dma_codes_2,
            layer_geometries,
        )

        for (
            layer_gisid,
            layer_shape_x,
            layer_shape_y,
            layer_dma_code_1,
            layer_dma_code_2,
            layer_geometry,
        ) in zipped_layer_data:
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

                new_pressure_control_valves.append(PressureControlValve(**data))

        PressureControlValve.objects.bulk_create(new_pressure_control_valves)
