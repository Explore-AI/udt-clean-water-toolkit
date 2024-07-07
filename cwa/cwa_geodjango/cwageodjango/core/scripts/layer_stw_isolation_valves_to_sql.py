from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping
from cwageodjango.assets.models import IsolationValve
from cwageodjango.utilities.models import DMA


class Command(BaseCommand):
    help = "Write Thames Water IsolationValve layer data to sql"

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

        isolation_valve_layer = ds[layer_index]

        new_isolation_valves = []
        for feature in isolation_valve_layer:
            gid = feature.get("tag")
            geom = feature.geom
            geom_4326 = feature.get("wkt_geom_4326")

            new_isolation_valve = IsolationValve(
                tag=gid, geometry=geom.wkt, geometry_4326=geom_4326
            )
            new_isolation_valves.append(new_isolation_valve)

            if len(new_isolation_valves) == 100000:
                IsolationValve.objects.bulk_create(new_isolation_valves)
                new_isolation_valves = []

        # save the last set of data as it will probably be less than 100000
        if new_isolation_valves:
            IsolationValve.objects.bulk_create(new_isolation_valves)

        DMAThroughModel = IsolationValve.dmas.through
        bulk_create_list = []
        for isolation_valve in IsolationValve.objects.only("id", "geometry"):
            wkt = isolation_valve.geometry.wkt

            dma_ids = DMA.objects.filter(geometry__intersects=wkt).values_list(
                "pk", flat=True
            )

            if not dma_ids:
                dma_ids = [DMA.objects.get(name=r"undefined").pk]

            bulk_create_list.extend(
                [
                    DMAThroughModel(isolationvalve_id=isolation_valve.pk, dma_id=dma_id)
                    for dma_id in dma_ids
                ]
            )

            if len(bulk_create_list) == 100000:
                DMAThroughModel.objects.bulk_create(bulk_create_list)
                bulk_create_list = []

        # save the last set of data as it will probably be less than 100000
        if bulk_create_list:
            DMAThroughModel.objects.bulk_create(bulk_create_list)
