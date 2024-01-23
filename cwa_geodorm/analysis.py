import setup  # Required. Do not remove.
from cwa_geod.config.settings import DEFAULT_SRID
from cwa_geod.network import GisToGraphNetwork


# https://github.com/ThamesWater/digitaltwin-refactor/blob/main/documentation/action-plan/action-plan-main.md
# https://thameswater.visualstudio.com/Data%20Factory%20-%20Default/_wiki/wikis/Data-Factory---Default.wiki/5545/Digital-Twin-Overview
# See examples folder
def clean_water_graph_from_gis_layers():
    gis_to_graph = GisToGraphNetwork(srid=DEFAULT_SRID)

    # for now it only creates the trunk mains networkx graph
    # nx_graph = gis_to_graph.create_network()
    nx_graph = gis_to_graph.create_network2()

    print(nx_graph)


def main():
    clean_water_graph_from_gis_layers()


main()
