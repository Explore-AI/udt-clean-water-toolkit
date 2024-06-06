from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from cwageodjango.assets.models import ConnectionMain
from cwageodjango.utilities.models import DMA


class Command(BaseCommand):
    help = "Write Thames Water connection mains layer data to sql"

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

        connection_main_layer = ds[layer_index]

        new_connection_mains = []
        for feature in connection_main_layer:
            gid = feature.get("GISID")
            geom = feature.geom
            geom_4326 = feature.get("wkt_geom_4326")
            material = feature.get("MATERIAL") or "unknown"
            diameter = feature.get("DIAMETER_mm")

            new_connection_main = ConnectionMain(
                gid=gid, geometry=geom.wkt, geometry_4326=geom_4326, material=material, diameter=diameter
            )
            new_connection_mains.append(new_connection_main)

            if len(new_connection_mains) == 100000:
                ConnectionMain.objects.bulk_create(new_connection_mains)
                new_connection_mains = []

        # save the last set of data as it will probably be less than 100000
        if new_connection_mains:
            ConnectionMain.objects.bulk_create(new_connection_mains)

        DMAThroughModel = ConnectionMain.dmas.through
        bulk_create_list = []
        for connection_main in ConnectionMain.objects.only("id", "geometry"):

            wkt = connection_main.geometry.wkt

            dma_ids = DMA.objects.filter(geometry__intersects=wkt).values_list(
                "pk", flat=True
            )

            if not dma_ids:
                dma_ids = [DMA.objects.get(name=r"undefined").pk]

            for dma_id in dma_ids:
                bulk_create_list.append(
                    DMAThroughModel(connectionmain_id=connection_main.pk, dma_id=dma_id)
                )

            if len(bulk_create_list) == 100000:
                DMAThroughModel.objects.bulk_create(bulk_create_list)
                bulk_create_list = []

        # save the last set of data as it will probably be less than 100000
        if bulk_create_list:
            DMAThroughModel.objects.bulk_create(bulk_create_list)
