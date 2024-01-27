from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from cwa_geod.assets.models import Chamber

CHAMBER_LAYER_INDEX = 31


class Command(BaseCommand):
    help = "Write Thames Water chamber layer data to sql"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="Path to gdb.zip")

    ### Attempt using bulk create
    def handle(self, *args, **kwargs):
        zip_path = kwargs.get("file")

        ds = DataSource(zip_path)
        chamber_layer = ds[CHAMBER_LAYER_INDEX]

        print(
            f"There are {chamber_layer.num_feat} features. Large numbers of features will take a long time to save."
        )

        layer_gisids = chamber_layer.get_fields("GISID")
        layer_shapes_x = chamber_layer.get_fields("SHAPEX")
        layer_shapes_y = chamber_layer.get_fields("SHAPEY")
        layer_geometries = chamber_layer.get_geoms()

        new_chambers = []
        for (
            layer_gisid,
            layer_shape_x,
            layer_shape_y,
            layer_geometry,
        ) in zip(
            layer_gisids,
            layer_shapes_x,
            layer_shapes_y,
            layer_geometries,
        ):
            data = {
                "gisid": layer_gisid,
                "shape_x": layer_shape_x,
                "shape_y": layer_shape_y,
                "geometry": layer_geometry.wkt,
            }

            if not None in data.values():
                new_chambers.append(Chamber(**data))

        Chamber.objects.bulk_create(new_chambers)
