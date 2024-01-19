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
    from django.contrib.gis.measure import D
    from django.db.models import OuterRef
    from django.contrib.postgres.expressions import ArraySubquery
    from django.db.models.functions import JSONObject
    from django.contrib.gis.db.models.functions import LineLocatePoint
    from cwa_geod.assets.models import Logger, TrunkMain

    # https://stackoverflow.com/questions/51102389/django-return-array-in-subquery
    # subquery = Logger.objects.filter(
    #     geometry__dwithin=(OuterRef("geometry"), D(m=1000))
    # ).values("id", "gisid", "geometry")

    subquery1 = Logger.objects.filter(
        geometry__dwithin=(OuterRef("geometry"), D(m=1000))
    ).values(json=JSONObject(id="id", gisid="gisid", geometry="geometry"))

    # subquery2 = (
    #     Logger.objects.filter(geometry__dwithin=(OuterRef("geometry"), D(m=1000)))
    #     .annotate(frac=LineLocatePoint(OuterRef("geometry"), geometry))
    #     .values(json=JSONObject(id="id", gisid="gisid", geometry="geometry"))
    # )

    x = TrunkMain.objects.annotate(logger_data=ArraySubquery(subquery))

    import pdb

    pdb.set_trace()

    print(nx_graph)


def main():
    clean_water_graph_from_gis_layers()


main()
