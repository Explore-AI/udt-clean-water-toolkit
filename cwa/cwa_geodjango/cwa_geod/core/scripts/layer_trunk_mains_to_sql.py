from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping
from cwa_geod.assets.models import TrunkMain
from cwa_geod.utilities.models import DMA


class Command(BaseCommand):
    help = "Write Thames Water trunk mains layer data to sql"

    def add_arguments(self, parser):
        parser.add_argument("-f", "--file", type=str, help="Path to valid datasource")
        parser.add_argument("-x", "--index", type=int, help="Layer index")

    def handle(self, *args, **kwargs):
        ds_path = kwargs.get("file")
        layer_index = kwargs.get("index")

        ds = DataSource(ds_path)

        print(
            f"""There are {ds[layer_index].num_feat} features.
Large numbers of features will take a long time to save."""
        )

        trunk_main_layer = ds[layer_index]

        layer_gis_ids = trunk_main_layer.get_fields("GISID")
        layer_geometries = trunk_main_layer.get_geoms()
        geometries_wkt = trunk_main_layer.get_fields("wkt_geom_4326")

        new_trunk_mains = []
        for gid, geom, geom_4326 in zip(layer_gis_ids, layer_geometries, geometries_wkt):

            new_trunk_main = TrunkMain(gid=gid, geometry=geom.wkt,
                                       geometry_4326=geom_4326)
            new_trunk_mains.append(new_trunk_main)

            if len(new_trunk_mains) == 100000:
                TrunkMain.objects.bulk_create(new_trunk_mains)
                new_trunk_mains = []


        # save the last set of data as it will probably be less than 100000
        if new_trunk_mains:
            TrunkMain.objects.bulk_create(new_trunk_mains)

        
        DMAThroughModel = TrunkMain.dmas.through
        bulk_create_list = []
        for trunk_main in TrunkMain.objects.only("id", "geometry"):

            wkt = trunk_main.geometry.wkt

            dma_ids = DMA.objects.filter(geometry__intersects=wkt).values_list(
                "pk", flat=True
            )

            if not dma_ids:
                dma_ids = [DMA.objects.get(name=r"undefined").pk]

            for dma_id in dma_ids:
                bulk_create_list.append(
                    DMAThroughModel(trunkmain_id=trunk_main.pk, dma_id=dma_id)
                )

        DMAThroughModel.objects.bulk_create(bulk_create_list, batch_size=120000)
