from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from cwa_geod.assets.models import OperationalSite
from cwa_geod.utilities.models import DMA

OPERATIONAL_SITE_LAYER_INDEX = 32


# for layermapping with foreign key
# https://stackoverflow.com/questions/21197483/geodjango-layermapping-foreign-key
class Command(BaseCommand):
    help = "Write Thames Water OperationalSite layer data to sql"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="Path to gdb.zip")

    ### Attempt using bulk create
    def handle(self, *args, **kwargs):
        zip_path = kwargs.get("file")

        ds = DataSource(zip_path)
        operational_site_layer = ds[OPERATIONAL_SITE_LAYER_INDEX]

        print(
            f"There are {operational_site_layer.num_feat} features. Large numbers of features will take a long time to save."
        )

        layer_gisids = operational_site_layer.get_fields("GISID")
        layer_shapes_x = operational_site_layer.get_fields("SHAPEX")
        layer_shapes_y = operational_site_layer.get_fields("SHAPEY")
        layer_geometries = operational_site_layer.get_geoms()

        new_operational_sites = []
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
                new_operational_sites.append(OperationalSite(**data))

                if len(new_operational_sites) == 100000:
                    OperationalSite.objects.bulk_create(new_operational_sites)
                    new_operational_sites = []

        # save the last set of data as it will probably be less than 100000
        if new_operational_sites:
            OperationalSite.objects.bulk_create(new_operational_sites)
