import setup  # Required. Do not remove.
import argparse
from cwa_geod.config.settings import DEFAULT_SRID
from cwa_geod.network import GisToNetworkX
#    from cwa_geod.config.db.graph_db import init_graphdb

# https://github.com/ThamesWater/digitaltwin-refactor/blob/main/documentation/action-plan/action-plan-main.md
# https://thameswater.visualstudio.com/Data%20Factory%20-%20Default/_wiki/wikis/Data-Factory---Default.wiki/5545/Digital-Twin-Overview
# See examples folder

#@init_graphdb
def cleanwater_gis2nx():
    import pdb; pdb.set_trace()

    gis_to_nx = GisToNetworkX(srid=DEFAULT_SRID)
    nx_graph = gis_to_nx.create_network2()

    print("Created Graph:", nx_graph)


# TODO: Deprecated. for test purposes only.
def create_pipes_network():
    # for now it only creates the trunk mains networkx graph
    # nx_graph = gis_to_graph.create_network()

    # new trial approach to create network
    gis_to_nx = GisToNetworkX(srid=DEFAULT_SRID)
    gis_to_nx.create_network()


def main():
    parser = argparse.ArgumentParser(description="Run Clean Water Toolkit functions")

    parser.add_argument(
        "--method", help="Convert the gis network to a connected graph network."
    )

    args = parser.parse_args()

    if args.method == "gis2nx":
        cleanwater_gis2nx()

    if args.method == "createpipes":
        create_pipes_network()


main()
