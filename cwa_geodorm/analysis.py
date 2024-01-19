import setup  # Required. Do not remove.
from cwa_geod.config.settings import DEFAULT_SRID
from cwa_geod.network import GisToGraphNetwork


# https://github.com/ThamesWater/digitaltwin-refactor/blob/main/documentation/action-plan/action-plan-main.md
# https://thameswater.visualstudio.com/Data%20Factory%20-%20Default/_wiki/wikis/Data-Factory---Default.wiki/5545/Digital-Twin-Overview
# See examples folder
def clean_water_graph_from_gis_layers():
    gis_to_graph = GisToGraphNetwork(srid=DEFAULT_SRID)

    # for now it only creates the trunk mains networkx graph
    nx_graph = gis_to_graph.create_network()

    # from custom_aggregates import JSONArrayAgg
    # from django.contrib.gis.db.models.functions import Distance
    # from django.contrib.gis.measure import D
    # from django.db.models import Value, JSONField
    # from django.db.models import OuterRef, Subquery
    # from django.contrib.gis.db.models.functions import AsGeoJSON, Cast
    # from cwa_geod.assets.models import Logger
    # from django.contrib.postgres.aggregates import ArrayAgg, StringAgg

    # from cwa_geod.assets.models import TrunkMain
    # from django.db.models import FilteredRelation, Q
    # x = TrunkMain.objects.prefetch_related("dma__dma_loggers").annotate(loggers_dist=FilteredRelation("dma__dma_loggers", condition=Q(geometry__dwithin=D(m=10000))))
    # geom = Logger.objects.first().geometry
    # x = Logger.objects.filter(geometry__dwithin=(geom, D(m=10000))).values_list(
    #     Cast(JSONArrayAgg("id"), output_field=JSONField())
    # )

    # x = (
    #     Logger.objects.filter(geometry__dwithin=(OuterRef("geometry"), D(m=10000)))
    #     .values("id")
    #     .annotate(ids=ArrayAgg("id"))
    #     .values("ids")
    # )
    # TrunkMain.objects.annotate(distances=Subquery(x))
    #     subquery = Logger.objects.filter(geometry__dwithin=(OuterRef("geometry"), D(m=10))).annotate(logger_ids=ArrayAgg('id')).values('logger_ids')
# TrunkMain.objects.annotate(distances=Subquery(subquery))
    import pdb

    # https://stackoverflow.com/questions/49570712/speeding-up-a-django-database-function-for-geographic-interpolation-of-missing-v
    # https://stackoverflow.com/questions/73668842/django-with-mysql-subquery-returns-more-than-1-row
    pdb.set_trace()

    print(nx_graph)


def main():
    clean_water_graph_from_gis_layers()


main()
