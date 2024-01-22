from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from cwa_geod.assets.models import NetworkOptValve
from cwa_geod.utilities.models import DMA

NETWORK_OPT_VALVE_LAYER_INDEX = 3
DMA_FIELD_NAME_1 = "DMA1CODE"
DMA_FIELD_NAME_2 = "DMA2CODE"


# for layermapping with foreign key
# https://stackoverflow.com/questions/21197483/geodjango-layermapping-foreign-key
class Command(BaseCommand):
    help = "Write Thames Water NetworkOptValve layer data to sql"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="Path to gdb.zip")

    ### Attempt using bulk create
    def handle(self, *args, **kwargs):
        zip_path = kwargs.get("file")

        ds = DataSource(zip_path)
        network_valve_layer = ds[NETWORK_OPT_VALVE_LAYER_INDEX]

        print(
            f"There are {network_valve_layer.num_feat} features. Large numbers of features will take a long time to save."
        )

        layer_gisids = network_valve_layer.get_fields("GISID")
        layer_shapes_x = network_valve_layer.get_fields("SHAPEX")
        layer_shapes_y = network_valve_layer.get_fields("SHAPEY")
        layer_dma_codes_1 = network_valve_layer.get_fields(DMA_FIELD_NAME_1)
        layer_geometries = network_valve_layer.get_geoms()

        new_network_valves = []
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
                "dma_1": layer_dma_code_1,
                "geometry": layer_geometry.wkt,
            }

            if not None in data.values():
                dma_1 = DMA.objects.get(code=data["dma_1"])
                data["dma_1"] = dma_1
                new_network_valves.append(NetworkOptValve(**data))

                if len(new_network_valves) == 100000:
                    NetworkOptValve.objects.bulk_create(new_network_valves)
                    new_network_valves = []

        # save the last set of data as it will probably be less than 100000
        if new_network_valves:
            NetworkOptValve.objects.bulk_create(new_network_valves)
