from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping
from cwageodjango.assets.models import ListeningPost
from cwageodjango.utilities.models import DMA


class Command(BaseCommand):
    help = "Write Thames Water ListeningPost layer data to sql"

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

        listening_post_layer = ds[layer_index]

        new_listening_posts = []
        for feature in listening_post_layer:
            gid = feature.get("tag")
            geom = feature.geom
            geom_4326 = feature.get("wkt_geom_4326")

            new_listening_post = ListeningPost(
                tag=gid, geometry=geom.wkt, geometry_4326=geom_4326
            )
            new_listening_posts.append(new_listening_post)

            if len(new_listening_posts) == 100000:
                ListeningPost.objects.bulk_create(new_listening_posts)
                new_listening_posts = []

        # save the last set of data as it will probably be less than 100000
        if new_listening_posts:
            ListeningPost.objects.bulk_create(new_listening_posts)

        DMAThroughModel = ListeningPost.dmas.through
        bulk_create_list = []
        for listening_post in ListeningPost.objects.only("id", "geometry"):
            wkt = listening_post.geometry.wkt

            dma_ids = DMA.objects.filter(geometry__intersects=wkt).values_list(
                "pk", flat=True
            )

            if not dma_ids:
                dma_ids = [DMA.objects.get(name=r"undefined").pk]

            bulk_create_list.extend(
                [
                    DMAThroughModel(listeningpost_id=listening_post.pk, dma_id=dma_id)
                    for dma_id in dma_ids
                ]
            )

            if len(bulk_create_list) == 100000:
                DMAThroughModel.objects.bulk_create(bulk_create_list)
                bulk_create_list = []

        # save the last set of data as it will probably be less than 100000
        if bulk_create_list:
            DMAThroughModel.objects.bulk_create(bulk_create_list)
