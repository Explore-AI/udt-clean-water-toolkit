from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from cwageodjango.assets.models import BulkMeter
from cwageodjango.utilities.models import DMA, Utility


class Command(BaseCommand):
    help = "Write Thames Water BulkMeter layer data to sql"

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

        bulk_meter_layer = ds[layer_index]

        # new_bulk_meters = []
        # for feature in bulk_meter_layer:
        #     gid = feature.get("tag")
        #     geom = feature.geom
        #     geom_4326 = feature.get("wkt_geom_4326")

        #     new_bulk_meter = BulkMeter(
        #         tag=gid, geometry=geom.wkt, geometry_4326=geom_4326
        #     )
        #     new_bulk_meters.append(new_bulk_meter)

        #     if len(new_bulk_meters) == 100000:
        #         BulkMeter.objects.bulk_create(new_bulk_meters)
        #         new_bulk_meters = []

        # # save the last set of data as it will probably be less than 100000
        # if new_bulk_meters:
        #     BulkMeter.objects.bulk_create(new_bulk_meters)

        # get the utility
        utility = Utility.objects.get(name="severn_trent_water")

        DMAThroughModel = BulkMeter.dmas.through
        bulk_create_list = []
        for bulk_meter in BulkMeter.objects.filter(dmas=None).only("id", "geometry"):
            wkt = bulk_meter.geometry.wkt

            dma_ids = DMA.objects.filter(
                geometry__intersects=wkt, utility=utility
            ).values_list("pk", flat=True)

            if not dma_ids:
                dma_ids = [DMA.objects.get(name=r"undefined", utility=utility).pk]

            bulk_create_list.extend(
                [
                    DMAThroughModel(bulkmeter_id=bulk_meter.pk, dma_id=dma_id)
                    for dma_id in dma_ids
                ]
            )

            if len(bulk_create_list) == 100000:
                DMAThroughModel.objects.bulk_create(bulk_create_list)
                bulk_create_list = []

        # save the last set of data as it will probably be less than 100000
        if bulk_create_list:
            DMAThroughModel.objects.bulk_create(bulk_create_list)
